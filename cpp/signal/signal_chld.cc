// This program shows that read can be interrupted with signal (e.g. SIGCHLD)
// if a signal is not ignored (e.g. A signal handler for SIGCHLD is registered.)
//
// This program outputs...
//   start child
//   end child
//   handler.
//   rc == -1
//   interrupted with signal!
//   end of main

#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h> 
#include <sys/wait.h>
#include <unistd.h>


void handler(int signum) {
  // Please note that we shouldn't call printf in signal handler
  // except for demo use because it's not "asynchronous-signal safe".
  printf("handler.\n");
}

int child() {
  printf("start child\n");
  sleep(1);
  printf("end child\n");
}

int main(int argc, char** argv) {
  int pid = fork();
  if (pid == 0) {
    child();
    return 0;
  }
  struct sigaction sa;
  memset(&sa, 0, sizeof(struct sigaction));
  sa.sa_handler = &handler;
  sigaction(SIGCHLD, &sa, NULL);
  char buf[256];
  ssize_t rc = read(fileno(stdin), (void*)buf, 256);
  // errno is thread-local.
  // http://www.kernel.org/doc/man-pages/online/pages/man3/errno.3.html
  if (rc < 0 && errno == EINTR) {
    printf("interrupted with signal!\n");
  }
  printf("end of main\n");
  return 0;
}
