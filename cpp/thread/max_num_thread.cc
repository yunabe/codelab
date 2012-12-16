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

static pthread_mutex_t block_mutex = PTHREAD_MUTEX_INITIALIZER;

void* waiting(void* data) {
  pthread_mutex_lock(&block_mutex);
  pthread_mutex_unlock(&block_mutex);
}

int main(int argc, char** argv) {
  int num = 16 * 1000;

  pthread_mutex_lock(&block_mutex);
  
  printf("Creating thread objects.\n");
  vector<pthread_t> threads(num);
  printf("Thread objects are created.\n");
  int max_index = -1;
  for (int i = 0; i < num; ++i) {
    int err = pthread_create(&threads[i], NULL, &waiting, NULL);
    if (err != 0) {
      printf("Failed to create a thread. (i == %d)\n", i);
      break;
    }
    max_index = i;
  }
  printf("All threads are started.\n");
  pthread_mutex_unlock(&block_mutex);
  printf("Released block_mutex.\n");
  for (int i = 0; i < max_index; ++i) {
    pthread_join(threads[i], NULL);
  }
}
