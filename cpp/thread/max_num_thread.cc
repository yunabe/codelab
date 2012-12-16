#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <vector>

using std::vector;

// Limit 1:
// # of process per user: ulimit -u
// --> Edit /etc/security/limits.conf
//
// Limit 2:
// /proc/sys/kernel/threads-max
// --> Edit /etc/sysctl.conf and run "sudo sysctl -p".
//
// Limit 3 (in 32 bit environment):
// Thread stack size * # of threads > virtual memory size.
//
// Limit 4
// https://listman.redhat.com/archives/phil-list/2003-August/msg00005.html
// /proc/sys/vm/max_map_count / 2 == max threads in one process.
// Add 'vm.max_map_count = XXX' to /etc/sysctl.conf.

class Barrier {
public:
  Barrier() : mutex_(PTHREAD_MUTEX_INITIALIZER),
              cond_(PTHREAD_COND_INITIALIZER),
              done_(false) {}

  void Wait() {
    pthread_mutex_lock(&mutex_);
    while (!done_) {
      pthread_cond_wait(&cond_, &mutex_);
    }
    pthread_mutex_unlock(&mutex_);
  }

  void Done() {
    pthread_mutex_lock(&mutex_);
    done_ = true;
    pthread_cond_broadcast(&cond_);
    pthread_mutex_unlock(&mutex_);
  }

private:
  pthread_mutex_t mutex_;
  pthread_cond_t cond_;
  bool done_;
};

void* waiting(void* data) {
  auto* barrier = static_cast<Barrier*>(data);
  barrier->Wait();
}

int main(int argc, char** argv) {
  int num = 1 * 1000;

  Barrier barrier;
  printf("Creating thread objects.\n");
  vector<pthread_t> threads(num);
  printf("Thread objects are created.\n");
  int max_index = -1;
  for (int i = 0; i < num; ++i) {
    int err = pthread_create(&threads[i], NULL, &waiting, &barrier);
    if (err != 0) {
      printf("Failed to create a thread. (i == %d)\n", i);
      break;
    }
    max_index = i;
  }
  printf("All threads are started.\n");
  barrier.Done();
  printf("barrier.Done.\n");
  for (int i = 0; i < max_index; ++i) {
    pthread_join(threads[i], NULL);
  }
}
