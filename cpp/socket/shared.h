#include <string>

void send_message(int sockfd, const std::string& msg);

std::string recv_message(int sockfd);
