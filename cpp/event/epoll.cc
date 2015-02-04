// g++ epoll.cc -o epoll && ./epoll
// http://man7.org/linux/man-pages/man7/epoll.7.html
// select, kqueue, epoll

// level-triggered? edge-triggered?

// http://man7.org/linux/man-pages/man2/signalfd.2.html

#include <iostream>
#include <sstream>

#include <sys/epoll.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>

const int MAX_EVENTS = 100;

const int NUM_WRITERS = 10;

void child_writer(int id, int fd) {
  std::ostringstream stream;
  sleep(id);
  stream << "[data from " << id << "]";
  std::string str = stream.str();
  write(fd, str.c_str(), str.size() + 1);
}

int main(int argc, char** argv) {
  int epfd = epoll_create(MAX_EVENTS);
  if (epfd < 0) {
    fprintf(stderr, "err: epoll_create()\\n");
    return -1;
  }

  int read_fds[NUM_WRITERS];
  for (int i = 0; i < NUM_WRITERS; ++i) {
    int rwfd[2];
    pipe(rwfd);
    if (fork() == 0) {
      fprintf(stderr, "Start of a child writer: %d\n", i);
      close(epfd);
      close(rwfd[0]);
      for (int j = 0; j < i; ++j) {
        close(read_fds[j]);
      }
      child_writer(i, rwfd[1]);
      fprintf(stderr, "End of a child writer: %d\n", i);
      return 0;
    } else {
      close(rwfd[1]);
      read_fds[i] = rwfd[0];
    }
  }

  for (int i = 0; i < NUM_WRITERS; ++i) {
    struct epoll_event event;
    memset(&event, 0, sizeof(event));
    event.events = EPOLLIN;
    event.data.fd = read_fds[i];
    // fd should not be regular file.
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, read_fds[i], &event) == -1) {
      int err = errno;
      fprintf(stderr, "error: epoll_ctl(): %d\n", err);
      // fprintf(stderr, "%d, %d, %d, %d, %d, %d, %d\n", EBADF, EEXIST, EINVAL, ENOENT, ENOMEM, ENOSPC, EPERM);
      return -1;
    }
  }

  int done_count = 0;
  while (done_count < NUM_WRITERS) {
    epoll_event events[MAX_EVENTS];
    int nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);
    for (int i = 0; i < nfds; ++i) {
      char buf[256];
      int n = read(events[i].data.fd, buf, 256);
      if (n == 0) {
        done_count++;
        epoll_ctl(epfd, EPOLL_CTL_DEL, events[i].data.fd, NULL);
      } else {
        fprintf(stderr, "Read: %s\n", buf);
      }
    }
  }

  close(epfd);
  return 0;
}
