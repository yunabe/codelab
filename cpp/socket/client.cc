#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <string>

#include "shared.h"

using std::string;

int main(int argc, char** argv) {
  int port = 9898;
  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(addr));
  addr.sin_port = htons(port);
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = inet_addr("127.0.0.1");
  int fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd == -1) {
    printf("Failed to open socket.\n");
    return 1;
  }
  int rc;
  rc = connect(fd, (struct sockaddr*)&addr, sizeof(addr));
  if (rc != 0) {
    printf("Failed to connect to the server.\n");
    return 1;
  }
  send_message(fd, "Hello!");
  close(fd);
  return 0;
}
