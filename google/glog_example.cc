#include <gflags/gflags.h>
#include <glog/logging.h>

DEFINE_int32(fibarg, 0, "");

int fib(int n);

int main(int argc, char** argv) {
  // Initialize Google's logging library.
  google::InitGoogleLogging(argv[0]);
  // Initialize Google's flags library to control behavior of logging library
  // by command line flags (e.g. --logtostderr).
  google::ParseCommandLineFlags(&argc, &argv, true);
  LOG(ERROR) << "Log message for LOG(ERROR)";
  LOG(WARNING) << "Log message for LOG(WARNING)";
  LOG(INFO) << "Log message for LOG(INFO)";
  VLOG(1) << "Log message for VLOG(1)";
  VLOG(2) << "Log message for VLOG(2)";
  fib(FLAGS_fibarg);
  return 0;
}
