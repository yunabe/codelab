#include <stdio.h>
#include <pthread.h>

typedef struct {
  pthread_mutex_t* mutex;
  pthread_cond_t* cond;
  int value;
} Shared;

const int LOOP_SIZE = 1000 * 1000;

void* Produce(void* data) {
  Shared* shared = data;
  for (int i = 0; i < LOOP_SIZE; i++) {
    pthread_mutex_lock(shared->mutex);
    if (shared->value >= 0) {
      pthread_cond_wait(shared->cond, shared->mutex);
    }
    shared->value = i;
    pthread_cond_signal(shared->cond);  // pthread_cond_broadcast?
    pthread_mutex_unlock(shared->mutex);
  }
  return NULL;
}

void* Consume(void* data) {
  Shared* shared = data;
  while (1) {
    pthread_mutex_lock(shared->mutex);
    if (shared->value < 0) {
      pthread_cond_wait(shared->cond, shared->mutex);
    }
    int i = shared->value;
    shared->value = -1;
    pthread_cond_signal(shared->cond);  // pthread_cond_broadcast?
    pthread_mutex_unlock(shared->mutex);
    if (i % (100 * 1000) == 0) {
      printf("i == %d\n", i);
    }
    if (i + 1 == LOOP_SIZE) {
      break;
    }
  }
  return NULL;
}

int main(int argc, char** argv) {
  pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
  pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

  Shared shared;
  shared.value = -1;
  shared.mutex = &mutex;
  shared.cond = &cond;
  pthread_t producer;
  pthread_create(&producer, NULL, &Produce, &shared);
  pthread_t consumer;
  pthread_create(&consumer, NULL, &Consume, &shared);

  pthread_join(producer, NULL);
  pthread_join(consumer, NULL);
  return 0;
}
