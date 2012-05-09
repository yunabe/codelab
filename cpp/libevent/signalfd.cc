#include <event.h>
#include <sys/signalfd.h>
#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
#include <set>

using std::set;

struct DataHolder {
  int sfd;
  set<pid_t> children;
};

void read_signalfd_cb(struct bufferevent *bev, void *ctx) {
  DataHolder* data = (DataHolder*)ctx;
  evbuffer* input = bufferevent_get_input(bev);
  signalfd_siginfo info;
  bool should_close = false;
  while (true) {
    int size = evbuffer_remove(input, (void *)&info, sizeof(info));
    if (size == 0) {
      break;
    }
    if (info.ssi_signo == SIGCHLD) {
      printf("Received SIGCHLD\n");
      pid_t pid = wait(NULL);
      if (data->children.find(pid) == data->children.end()) {
        printf("Unexpected pid: %d\n", pid);
      } else {
        data->children.erase(pid);
      }
      if (data->children.size() == 0) {
        printf("Removed all childrens...\n");
        close(data->sfd);
        // close is not good enough to exit from loop in some cases.
        // TODO(yunabe): Understand the reason.
        event_loopexit(0);
      }
    } else if (info.ssi_signo == SIGINT) {
      printf("Received SIGINT\n");
      break;
    }
  }
}

int read_signalfd(DataHolder* data) {
  bufferevent* bufev = bufferevent_new(data->sfd, &read_signalfd_cb,
                                       NULL, NULL, data);
  bufferevent_enable(bufev, EV_READ);
}

int main(int argc, char** argv) {
  DataHolder data;
  event_init();
  sigset_t sigset;
  sigfillset(&sigset);
  sigprocmask(SIG_BLOCK, &sigset, NULL);
  data.sfd = signalfd(-1, &sigset, 0);
  read_signalfd(&data);
  
  for (int i = 0; i < 5; ++i) {
    pid_t pid = fork();
    if (pid == 0) {
      sleep(i + 1);
      close(data.sfd);
      printf("End of child - %d\n", i);
      return 0;
    } else {
      data.children.insert(pid);
    }
  }
  event_dispatch();
  printf("End of program\n");
  return 0;
}
