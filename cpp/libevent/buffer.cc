#include <event.h>
#include <unistd.h>
#include <stdio.h>
#include <vector>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

using std::vector;

void write_data(int id, int fd) {
  FILE* f = fdopen(fd, "w");
  for (int i = 0; i < 5; ++i) {
    fprintf(f, "write (id == %d, i == %d)\n", id, i);
    fflush(f);
    sleep(1);
  }
  fclose(f);
}

void read_cb(struct bufferevent *bev, void *ctx) {
  evbuffer* input = bufferevent_get_input(bev);
  char *line;
  size_t n;
  while ((line = evbuffer_readln(input, &n, EVBUFFER_EOL_LF))) {
    printf("line == %s\n", line);
    free(line);
  }
}

void read_data(int fd) {
  bufferevent* bufev = bufferevent_new(fd, &read_cb, NULL, NULL, NULL);
  bufferevent_enable(bufev, EV_READ);
}

int main(int argc, char** argv) {
  event_init();
  vector<pid_t> pids;
  vector<int> rpipes;
  for (int i = 0; i < 3; ++i) {
    int pipefd[2];
    pipe(pipefd);
    pid_t pid = fork();
    if (pid == 0) {
      close(pipefd[0]);
      write_data(i, pipefd[1]);
      return 0;
    } else {
      close(pipefd[1]);
      rpipes.push_back(pipefd[0]);
      read_data(pipefd[0]);
      pids.push_back(pid);
    }
  }
  event_dispatch();
  for (int i = 0; i < pids.size(); ++i) {
    waitpid(pids[i], NULL, 0);
  }
  return 0;
}
