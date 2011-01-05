#include <gflags/gflags.h>
#include <glog/logging.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <string>
#include <sys/types.h>
#include <unistd.h>
#include <vector>
#include <dirent.h>
#include <dlfcn.h>
#include <sys/mman.h>

#include "os.h"
#include "strutil.h"

using std::string;
using std::vector;

DEFINE_string(hotpatch_library_dir,
              "A directory from which the program loads shared libraries.",
              "");

namespace {

  void GetFunctionNames(const string& path, vector<string>* list) {
    // Extracts function names in shared library using nm command.
    string command = strutil::format("nm -D %s", path.c_str());
    FILE* p = popen(command.c_str(), "r");
    char buffer[1000];
    while (fgets(buffer, 1000, p)) {
      if (buffer[0] == '\0') {
        return;
      }
      vector<string> entries;
      strutil::split(buffer, ' ', &entries);
      if (entries.size() != 3) {
        continue;
      }
      if (entries[1] != "T") {
        continue;
      }
      const string name = strutil::rstrip(entries[2]);
      if (name == "_init" || name == "_fini") {
        continue;
      }
      list->push_back(name);
    }
    pclose(p);
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

  bool HotpatchSharedLibrary(const string& library, string* error) {
    void* handle;
    // Checks if library has been loaded.
    // Note that we need to use RTLD_NOW.
    if (handle = dlopen(library.c_str(), RTLD_NOLOAD | RTLD_NOW)) {
      LOG(INFO) << library << " has already been loaded. closing...";
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
    GetFunctionNames(library, &names);
    for (int i = 0; i < names.size(); ++i) {
      const string& name = names[i];
      void* original_sym = dlsym(NULL, name.c_str());
      void* new_sym = dlsym(handle, name.c_str());
      if (original_sym == NULL || new_sym == NULL) {
        LOG(ERROR) << name << ": " << original_sym << ":" << new_sym;
        continue;
      }
      string divert_error;
      LOG(INFO) << "Divert function call: " << name;
      if (!DivertFunctionCall((char*)original_sym, (char*)new_sym,
                              &divert_error)) {
        *error = "Failed to divert: " + name + " (" + divert_error + ")";
        return false;
      };
    }
    return true;
  }

  void handle_signal(int sig, siginfo_t* info, void* ctx) {
    LOG(INFO) << "handle_signal is called.";
    vector<string> files;
    if (!os::listdir(FLAGS_hotpatch_library_dir, &files)) {
      return;
    }
    for (int i = 0; i < files.size(); ++i) {
      const string& file = files[i];
      if (file.rfind(".so") != file.size() - 3) {
        continue;
      }
      string path =
        os::path::abspath(os::path::join(FLAGS_hotpatch_library_dir, file));
      string error;
      LOG(INFO) << "Hotpatching " << path;
      if (!HotpatchSharedLibrary(path, &error)) {
        LOG(ERROR) << "Failed to hotpatch " << path << ": " << error;
      }
    }
  }

  class Initializer {
  public:
    Initializer() {
      if (FLAGS_hotpatch_library_dir.empty()) {
        LOG(ERROR) << "--hotpatch_library_dir is empty.";
        return;
      }
      LOG(INFO) << "Initializing hotpatch module [pid = " << getpid() << "].";
      struct sigaction act;
      memset(&act, 0, sizeof(struct sigaction));
      act.sa_sigaction = &handle_signal;
      act.sa_flags = SA_SIGINFO | SA_RESTART;
      if (sigaction(SIGALRM, &act, NULL) != 0) {
        LOG(FATAL) << "Failed to register a signal handler.";
      }
    }
  };

  Initializer initializer;
}  // namespace
