#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>

#include <string>

using std::string;

void send_message(int sockfd, const string& msg) {
  int offset = 0;
  while (offset <= msg.size()) {
    int size = send(sockfd, msg.c_str() + offset, msg.size() + 1 - offset, 0);
    if (size <= 0) {
      printf("Failed to send message: size = %d\n", size);
    } else {
      printf("Sent message: size = %d\n", size);
    }
    offset += size;
  }
}

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
