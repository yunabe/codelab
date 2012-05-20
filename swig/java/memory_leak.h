#include <stdio.h>
#include <memory>

class Runner {
 public:
  Runner() {};
  virtual void run() const {
    printf("Runner:run()\n");
  };

  virtual ~Runner() {}
};

class Manager {
 public:
  void set_runner(Runner* runner) {
    runner_.reset(runner);
  }

  void run() {
    if (runner_.get() != NULL) {
      return runner_->run();
    }
  }

 private:
  std::auto_ptr<Runner> runner_;
};
