#include <stdio.h>

#include <map>
#include <string>
#include <vector>

using std::vector;
using std::map;
using std::string;

void iteration() {
  // initialization list
  vector<int> list{1, 2, 3};
  // You can get rid of a whitespace between > and > in C++ 11.
  vector<vector<int> > nested{{1}, {2, 3}, {4, 5, 6}};

  // range based for
  for (int val : list) {
    printf("list[?] == %d\n", val);
  }
  for (auto& entry : nested) {
    printf("(len(entry), entry[0]) == (%zd, %d)\n", entry.size(), entry[0]);
  }

  map<string, string> mm{{"a", "b"}, {"c", "d"}};
  for (auto& pair : mm) {
    printf("key: %s, val: %s\n", pair.first.c_str(), pair.second.c_str());
  }
}

void null_pointer() {
  int* p = nullptr;
  int* q = NULL;

  // compile error
  // int r = nullptr;
  // OK
  int s = NULL;

  // compile error
  // s == nullptr;
  // OK
  s == NULL;
}

// unscoped enum
enum OldEnum {VAL0, VAL1};

// scoped enum. "class" can be "struct".
enum class NewEnum {VAL0, VAL1};

enum class  ScopedEnumWithType : long long {VAL0, VAL1};
enum UnscopedEnumWithType : long long {VAL2, VAL3};

// Forward declaration with type.
enum class ScopedDeclaredEnum: int;  // ": int" is optional.
enum UnscopedDeclaredEnum: int;

void enum_cpp11() {
  printf("VAL0: %d\n", VAL0);
  printf("VAL1: %d\n", VAL1);
  printf("NewEnum::VAL0: %d\n", NewEnum::VAL0);
  printf("NewEnum::VAL1: %d\n", NewEnum::VAL1);

  // OK. VAL0 is int.
  if (VAL0 == 0) {}
  // compile error
  // if (NewEnum::VAL0 == 0) {}
}

int main(int argc, char** argv) {
  int x = 2;
  auto y = x;  // int y = x;
  auto& z = x;  // int& z = x;
  x = 3;
  printf("y == %d\n", y);
  printf("z == %d\n", z);

  iteration();
  null_pointer();
  enum_cpp11();
  return 0;
}
