#include <gflags/gflags.h>
#include <stdio.h>

DEFINE_string(name, "world", "Username. Says hello to this user.");

static bool ValidateName(const char* flagname, const std::string& value) {
  if (value.length() > 10) {
    fprintf(stderr, "Value for --%s: %s is too long.\n",
            flagname, value.c_str());
    return false;
  }
  return true;
}

// Defines dummy variable to call RegisterFlagValidator.
static const bool name_dummy =
  google::RegisterFlagValidator(&FLAGS_name, &ValidateName);

void say_hello() {
  printf("Hello %s.\n", FLAGS_name.c_str());
}
