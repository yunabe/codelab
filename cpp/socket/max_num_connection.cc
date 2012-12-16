#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <vector>

using std::vector;

static const int kNum = 5000;
static const int kPort = 9898;

int server() {
  int fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd == -1) {
    printf("Failed to open socket.");
    return 1;
  }
  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(addr));
  addr.sin_port = htons(kPort);
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = htonl(INADDR_ANY);

  int on = 1;
  setsockopt(fd, SOL_SOCKET, SO_REUSEADDR,
             (const void*)&on, sizeof(on));

  int rc;
  rc = bind(fd, (struct sockaddr *)&addr, sizeof(addr));
  if (rc != 0) {
    printf("Failed to bind addr.\n");
    return 1;    
  }
  rc = listen(fd, 1);
  if (rc != 0) {
    printf("Failed to listen socket.\n");
    return 1;
  }
  struct sockaddr_in client;
  socklen_t client_size = sizeof(client);
  int count = 0;
  vector<int> clients;
  while (true) {
    int cl = accept(fd, (struct sockaddr *)&client, &client_size);
    if (cl == -1) {
      printf("Failed to accept connection (count == %d).\n", count);
      perror("perror0");
      break;
    }
    clients.push_back(cl);
    ++count;
    if (count == kNum) {
      break;
    }
  }
  printf("Closing connections in server\n");
  fflush(stdout);
  for (int i = 0; i < clients.size(); ++i) {
    close(clients[i]);
  }
  return 0;
}

int client() {
  vector<int> descriptors;
  for (int index = 0; index < kNum; ++index) {
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_port = htons(kPort);
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd == -1) {
      printf("Failed to open socket.\n");
      perror("perror1");
      break;
    }
    int rc;
    rc = connect(fd, (struct sockaddr*)&addr, sizeof(addr));
    if (rc != 0) {
      printf("Failed to connect to the server. (index == %d)\n", index);
      perror("perror2");
      break;
    }
    descriptors.push_back(fd);
  }
  printf("Closing connections in client\n");
  fflush(stdout);
  for (int i = 0; i < descriptors.size(); ++i) {
    close(descriptors[i]);
  }
  return 0;
}

int main(int argc, char** argv) {
  pid_t pid = fork();
  if (pid == 0) {
    return client();
  } else {
    return server();
  }
}
