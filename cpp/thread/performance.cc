// g++ performance.cc -o performance -lpthread -std=c++0x && time ./performance

#include <pthread.h>
#include <stdio.h>
#include <vector>
#include <sys/time.h>

using std::vector;

static const int kNumThread = 4;

static const int kInput = 39;

int naive_fib(int n) {
  if (n < 2) {
    return 1;
  }
  return naive_fib(n - 1) + naive_fib(n - 2);
}

static vector<int> exec_times;
pthread_mutex_t exec_times_mutex = PTHREAD_MUTEX_INITIALIZER;

void* thread_routine(void* ptr) {
  timeval tv0, tv1;
  gettimeofday(&tv0, NULL);
  naive_fib(kInput);
  gettimeofday(&tv1, NULL);
  int msec = (tv1.tv_sec - tv0.tv_sec) * 1000 +
    (tv1.tv_usec - tv0.tv_usec) / 1000;
  pthread_mutex_lock(&exec_times_mutex);
  exec_times.push_back(msec);
  pthread_mutex_unlock(&exec_times_mutex);
}

int main(int argc, char** argv) {
  vector<pthread_t> threads(kNumThread);
  int max_index = -1;
  for (int i = 0; i < kNumThread; ++i) {
    int err = pthread_create(&threads[i], NULL, &thread_routine, NULL);
    if (err != 0) {
      printf("Failed to create a thread. (i == %d)\n", i);
      break;
    }
    max_index = i;
  }
  for (int i = 0; i <= max_index; ++i) {
    pthread_join(threads[i], NULL);
  }
  for (int i = 0; i < exec_times.size(); ++i) {
    printf("%d\n", exec_times[i]);
  }
  return 0;
}
