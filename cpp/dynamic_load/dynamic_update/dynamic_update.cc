#include "dynamic_update.h"

#include <bfd.h>
#include <dlfcn.h>
#include <map>
#include <string>
#include <vector>
#include <string.h>
#include <stdio.h>
#include <sys/mman.h>

using std::map;
using std::string;
using std::vector;

namespace {

bool GetFunctionNames(const string& library,
                      vector<string>* names,
                      string* error) {
  bfd* abfd = bfd_openr(library.c_str(), NULL);
  if (abfd == NULL) {
    *error = "bfd_openr returned NULL.";
    return false;
  }
  bfd_check_format(abfd, bfd_object);
  asymbol* store = bfd_make_empty_symbol(abfd);
  void* minisyms;
  size_t size;
  int symcount = bfd_read_minisymbols(abfd, 0, &minisyms,
                                      (unsigned int*)(&size));
  bfd_byte* from = (bfd_byte*)minisyms;
  bfd_byte* fromend = from + symcount * size;
  for (; from < fromend; from += size) {
    asymbol* sym = bfd_minisymbol_to_symbol(abfd, 0, from, store);
    const char* name =bfd_asymbol_name(sym);
    if (sym->flags != (BSF_FUNCTION | BSF_GLOBAL)) {
      continue;
    }
    if (strcmp(name, "_init") == 0 || strcmp(name, "_fini") == 0) {
      continue;
    }
    names->push_back(name);
  }
  return true;
}

bool DivertFunctionCall(char *dst, char* code, string* error) {
  // TODO: This implementation is too simple.
  // Is there any way to guarantee that each function has more than 5
  // (12 for x86_64) bytes?
  int pagesize = sysconf(_SC_PAGE_SIZE);
  char* head = (char *)((unsigned long)dst / pagesize * pagesize);
  int size = dst - head + 5;
  if(mprotect(head, size, PROT_WRITE | PROT_EXEC) == -1) {
    *error = "Failed to mprotect.";
    return false;
  }
#if defined(__i386__)
  int diff = code - dst - 5;
  if (code != dst + 5 + diff) {
    return false;
  }
  dst[0] = 0xe9;
  dst++;
  *((int *)dst) = diff;
#endif
#if defined(__x86_64__)
  // movq $0x<64bit addr>, %rax
  // jmp *%rax
  // I feel there might be more efficient way that consume less than 12 bytes.
  dst[0] = 0x48;
  dst[1] = 0xb8;
  *(void **)(dst + 2) = code;
  dst[10] = 0xff;
  dst[11] = 0xe0;
#endif
  return true;
}
}

bool HotpatchSharedLibrary(const string& library, string* error) {
  void* handle;
  // Checks if library has been loaded.
  // Note that we need to use RTLD_NOW.
  if (handle = dlopen(library.c_str(), RTLD_NOLOAD | RTLD_NOW)) {
    for (int i = 0; i < 2; ++i) {
      dlclose(handle);
    }
  }
  handle = dlopen(library.c_str(), RTLD_NOW);
  if (handle == NULL) {
    *error = dlerror();
    return false;
  }
  vector<string> names;
  if (!GetFunctionNames(library, &names, error)) {
    return false;
  }
  for (int i = 0; i < names.size(); ++i) {
    const string& name = names[i];
    void* original_sym = dlsym(NULL, name.c_str());
    void* new_sym = dlsym(handle, name.c_str());
    if (original_sym == NULL || new_sym == NULL) {
      continue;
    }
    string divert_error;
    if (!DivertFunctionCall((char*)original_sym, (char*)new_sym,
                            &divert_error)) {
      *error = "Failed to divert: " + name + " (" + divert_error + ")";
      return false;
    };
  }
  return true;
}
