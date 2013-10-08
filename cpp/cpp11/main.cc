#include <stdio.h>

#include <map>
#include <memory>  // auto_ptr, unique_ptr
#include <string>
#include <vector>

using std::auto_ptr;
using std::vector;
using std::map;
using std::string;
using std::unique_ptr;


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

void unique_pointer() {
  unique_ptr<int> up0;
  up0.reset(new int);
  // compile error
  // unique_ptr<int> up1(up0);
  unique_ptr<int> up1(std::move(up0));
  // We need to move the pointer explicitly :)
  printf("up0.get() == %p\n", up0.get());
  printf("up1.get() == %p\n", up1.get());

  vector<unique_ptr<int> > uni_vec;
  uni_vec.push_back(unique_ptr<int>(new int(10)));
  uni_vec.emplace_back(new int(20));
  // compile error!
  // uni_vec.push_back(new int(10));

  // FYI: auto_ptr. auto_ptr is deprecated.
  auto_ptr<int> ap0;
  ap0.reset(new int);
  auto_ptr<int> ap1(ap0);  // This moves the pointer from ap0 to ap1.
  // std::move style is also fine in C++ 11 though auto_ptr is deprecated.
  // auto_ptr<int> ap1(std::move(ap0));
  printf("ap0.get() == %p\n", ap0.get());
  printf("ap1.get() == %p\n", ap1.get());

  // FYI: auto_ptr in containers (anyway, auto_ptr is deprecated.)
  vector<auto_ptr<int> > auto_vec;
  // compile error in C++03 but compilable in C++ 11
  // (because push_back receive T&&?).
  auto_vec.push_back(auto_ptr<int>(new int (10)));

  // compile error in C++11 too.
  // auto_vec.push_back(ap1);
  auto_vec.push_back(std::move(ap1));

  printf("ap1.get() == %p\n", ap1.get());  // (nil)
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
  unique_pointer();
  return 0;
}
