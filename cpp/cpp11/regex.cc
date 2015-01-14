#include <iostream>
#include <regex>

using std::cout;
using std::endl;

int main(int argc, char** argv) {
  std::regex re("a(b+)(c)");
  std::cmatch matches;
  if (!std::regex_match("abbbc", matches, re)) {
    cout << "No match" << endl;
    return 1;
  }
  for (int i = 0; i < matches.size(); ++i) {
    cout << "matches[" << i << "] == "
         << matches[i] << endl;
  }
  return 0;
}
