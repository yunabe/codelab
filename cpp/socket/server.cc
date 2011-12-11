#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

#include <string>

using std::string;

string recv_message(int sockfd) {
  string result;
  char buf[2];
  while (true) {
    int size = recv(sockfd, &buf, 2, 0);
    if (size <= 0) {
      printf("Failed to recv data: size == %d\n", size);
      break;
    }
    result.append(buf, 0, size);
  }
  return result;
}

void send_message(int sockfd, const string& msg) {
  int offset = 0;
  while (offset <= msg.size()) {
    int size = send(sockfd, msg.c_str() + offset, msg.size() + 1 - offset, 0);
    if (size <= 0) {
      printf("Failed to send message: size = %d\n", size);
    }
    offset += size;
  }
}

int main(int argc, char** argv) {
  int port = 9898;
  int fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd == -1) {
    printf("Failed to open socket.");
    return 1;
  }
  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(addr));
  addr.sin_port = htons(port);
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
  while (true) {
    int cl = accept(fd, (struct sockaddr *)&client, &client_size);
    if (cl == -1) {
      printf("Failed to accept connection.\n");
      return 1;    
    }
    printf("Recieved message: %s\n", recv_message(cl).c_str());
  }
  return 0;
}
