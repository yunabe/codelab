#include <gflags/gflags.h>
#include <unistd.h>

// Use DECLARE_type when you want to use the flag in different file.
DECLARE_string(name);

DEFINE_bool(overwrite_name, false, "Overwrite name with login name.");

void say_hello();

int main(int argc, char** argv) {
  google::ParseCommandLineFlags(&argc, &argv, true);
  if (FLAGS_overwrite_name) {
    FLAGS_name = getlogin();
  }
  say_hello();
  return 0;
}
