// It took about 40ns to lock and unlock a mutex (on virtual machine).
// So, if no confilict (or probability or conflic is low),
// the impact of mutex overhead is limited.

#include <pthread.h>

int main( int argc, char ** argv ) {
  int loop = 100 * 1000 * 1000;
  pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
  for (int i = 0; i < loop; ++i) {
    pthread_mutex_lock(&mutex);
    pthread_mutex_unlock(&mutex);
  }
  pthread_mutex_destroy(&mutex);
  return 0;
}
