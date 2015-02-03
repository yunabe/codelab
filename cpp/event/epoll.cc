// g++ epoll.cc -o epoll && ./epoll
// http://man7.org/linux/man-pages/man7/epoll.7.html
// select, kqueue, epoll

// level-triggered? edge-triggered?

// http://man7.org/linux/man-pages/man2/signalfd.2.html

#include <sys/epoll.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>

const int MAX_EVENTS = 10;

int main(int argc, char** argv) {
  int epfd = epoll_create(MAX_EVENTS);
  if (epfd < 0) {
    fprintf(stderr, "err: epoll_create()\\n");
    return -1;
  }

  int rwfd[2];
  pipe(rwfd);
  if (fork() == 0) {
    close(epfd);
    close(rwfd[0]);
    write(rwfd[1], "hogehogehoge", 10);
    fprintf(stderr, "end of child\n");
    return 0;
  } else {
    close(rwfd[1]);
  }

  struct epoll_event event;
  memset(&event, 0, sizeof(event));
  event.events = EPOLLIN;
  event.data.fd = rwfd[0];
  // fd should not be regular file.
  if (epoll_ctl(epfd, EPOLL_CTL_ADD, rwfd[0], &event) == -1) {
    int err = errno;
    fprintf(stderr, "error: epoll_ctl(): %d\n", err);
    // fprintf(stderr, "%d, %d, %d, %d, %d, %d, %d\n", EBADF, EEXIST, EINVAL, ENOENT, ENOMEM, ENOSPC, EPERM);
    return -1;
  }

  while (true) {
    epoll_event events[MAX_EVENTS];
    int nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);
    fprintf(stderr, "nfds == %d\n", nfds);
    bool done = false;
    for (int i = 0; i < nfds; ++i) {
      char buf[256];
      int n = read(events[i].data.fd, buf, 256);
      fprintf(stderr, "read %d bytes.\n", n);
      if (n == 0) {
        done = true;
      }
    }
    if (done) {
      break;
    }
  }

  close(epfd);
  return 0;
}
