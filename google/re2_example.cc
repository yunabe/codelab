#include <iostream>
#include <string>
#include <re2/re2.h>
#include <re2/stringpiece.h>

// re2::RE2 is not needed because re2::RE2 has been declared in re2/re2.h
using std::string;
using re2::StringPiece;

#define O(message) std::cout << #message << " = " <<\
                   std::boolalpha << message << std::endl;

int main(int argc, char** argv) {
  O(RE2::FullMatch("hello", "h.*o"));
  O(RE2::FullMatch("hello", "e"));
  O(RE2::PartialMatch("hello", "h.*o"));
  O(RE2::PartialMatch("hello", "e"));

  // Pre-compiled regex
  RE2 re("(\\w+):(\\d+)");
  int i;
  string s;
  // Submatch extraction
  O(RE2::FullMatch("ruby:1234", re, &s, &i));
  std::cout << "Result: i = " << i << ", s = " << s << std::endl;

  // Sequential match with Consume and StringPiece.
  string content = "x=10,y=20, z=10";
  StringPiece input(content);
  string key, value;
  std::cout << "A example of RE2::Consume" << std::endl;
  while (RE2::Consume(&input, "(\\w+)=(\\w+),?", &key, &value)) {
    // z=10 won't be captured because Consume anchors a match at the beginning
    // of input.
    std::cout << "key = " << key << ", value = " << value << std::endl;
  }
  std::cout << "A example of RE2::FindAndConsume" << std::endl;
  input = content;
  while (RE2::FindAndConsume(&input, "(\\w+)=(\\w+),?", &key, &value)) {
    // z=10 will also be captured if we use FindAndConsume.
    std::cout << "key = " << key << ", value = " << value << std::endl;
  }
  return 0;
}
