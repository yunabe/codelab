// Learning C++ template programming.
// g++ template.cc -std=c++11 -o template && ./template

#include <stdio.h>
#include <iostream>
#include <typeinfo>
#include <string>

// Function template.
// `typename` can be `class` though T can be instantiated with primitive types
// like int.
template <typename T> T add(T x, T y) {
  return x + y;
}

// Function overloading works with templates.
template <typename T> T add(T x, T y, T z) {
  return x + y + z;
}

// Normal function overloading.
// Non-template version is preferred over template version.
std::string add(std::string x, std::string y) {
  return "[" + x + + "|" + y + "]";
}

// Template declaration.
template <typename T> T get_value();

// Template specialization:
// <int> after add is optional because the compiler can infer it.
// Non-specialized template declaration/definition is necessary before
// template specialization.
template <> int get_value<int>() {
  return 42;
}

template <> double get_value() {
  return 4.2;
}

void play_with_function_template() {
  std::cout << "=== play_with_function_template ===" << std::endl;
  std::cout << "add<int>(3, 4) == " << add<int>(3, 4) << std::endl;
  std::cout << "add<double>(3.4, 4) == " << add<double>(3.4, 4) << std::endl;
  // C++ compiler deduces template arguments of function template.
  // http://en.cppreference.com/w/cpp/language/template_argument_deduction
  std::cout << "add(3, 4) == " << add(3, 4) << std::endl;

  // Function overloading with template and deduction.
  std::cout << "add(3, 4, 5) == " << add(3, 4, 5) << std::endl;
  // Normal function overloading. Non-template version is invoked.
  std::cout << "add(3, 4, 5) == "
            << add(std::string("foo"), std::string("bar")) << std::endl;

  // This causes a compile error! (e.g. 'T' ('double' vs. 'int'))
  // std::cout << "add(3.0, 4) == " << add(3.0, 4) << std::endl;

  // You can not drop <int> because template arguments are not deduced
  // from the function output type.
  int int_val = get_value<int>();
  std::cout << "get_value<int>() == " << int_val << std::endl;
  double double_val = get_value<double>();
  std::cout << "get_value<double>() == " <<  double_val << std::endl;

  // This causes a link error.
  // get_value<char>();
}

// Templates with values.
template <int val> int addVal(int x) {
  return x + val;
}

// Template-metaprogramming
template <int n> int metafib() {
  return metafib<n - 1>() + metafib<n - 2>();
}

template <> int metafib<0>() {
  return 1;
}

template <> int metafib<1>() {
  return 1;
}

void play_with_template_with_value() {
  std::cout << "=== play_with_template_with_value ===" << std::endl;
  std::cout << "addVal<7>(4) == " << addVal<7>(4) << std::endl;
  std::cout << "metafib == " << metafib<10>() << std::endl;
}

// Variadic templates (since C++11).
// http://eli.thegreenplace.net/2014/variadic-templates-in-c/

// You must define this before the next variadic template.
// `index` is very important even if it's not used because
template <int index> void variadic_temp_func() {}

template <int index, typename T, typename... Rest>
void variadic_temp_func(T t, Rest... rest) {
  std::cout << index << ": " << t << std::endl;
  variadic_temp_func<index + 1, Rest...>(rest...);
}

template <typename... Rest>
void variadic_temp_func(Rest... rest) {
  variadic_temp_func<0, Rest...>(rest...);
}

void play_with_variadic_template() {
  std::cout << "=== play_with_variadic_template ===" << std::endl;
  variadic_temp_func(1, 3, "hello", 4.5);
}

// Class template.
template <typename T, typename U>
class MyClass {
public:
  T t;
  U u;
};

// Class template declaration.
template <typename T> class B;

template <typename T>
class A {
public:
  A(T x) {
    std::cout << "A::A(" << x << ");" << std::endl;
  }

  // Method template
  template <typename K>
  void printK(K k) {
    std::cout << "printK:" << k << "(T: " << typeid(T).name() << ", K: "
              << typeid(K).name() << ")" << std::endl;
  }

  B<T>* b;
};

template <typename T> A<T>* makeA(T x) {
  return new A<T>(x);
}

// Template alias (Since C++11).
template <typename T>
using AliasA = A<T>;

void play_with_class_template() {
  std::cout << "=== play_with_class_template ===" << std::endl;
  // `auto* ap = new A(3);` is an error.
  // Template parameter of the class is not deduced by
  // the arguments of the constructor.
  // That's why a function like make_pair is useful.
  auto* pi = makeA(3);
  auto* ps = makeA("hello");

  pi->printK("'K'");
  ps->printK('K');

  delete pi;
  delete ps;
}

//////////////////////////////////////////////
/// Implement Tuple with variadic template ///
//////////////////////////////////////////////

// The helper class to get n'th type.
template <int n, typename Head, typename... Tail> struct NthType {
  typedef typename NthType<n - 1, Tail...>::type type;
};

// Template-specialization (n == 0).
template <typename Head, typename... Tail> struct NthType<0, Head, Tail...> {
  typedef Head type;
};

// Declaration of Tuple.
template <typename Head, typename... Tail> class Tuple;

// The helper class to get n'th value from a Tuple.
template <int n, typename Head, typename... Tail> struct TupleGetHelper {
  static const typename NthType<n, Head, Tail...>::type&
  get(const Tuple<Head, Tail...>& tuple) {
    return TupleGetHelper<n - 1, Tail...>::get(tuple.tail_);
  }
};

// Template-specialization (n == 0).
template <typename Head, typename... Tail> struct TupleGetHelper<0, Head, Tail...> {
  static const Head&
  get(const Tuple<Head, Tail...>& tuple) {
    return tuple.value_;
  }
};

// Definition of Tuple.
template <typename Head, typename... Tail>
class Tuple {
public:
  Head value_;
  Tuple<Tail...> tail_;

  explicit Tuple(Head value, Tail... tail) : value_(value), tail_(tail...) {}

  template <int n>
  const typename NthType<n, Head, Tail...>::type&
  get() const {
    return TupleGetHelper<n, Head, Tail...>::get(*this);
  }
};

// Template specialization of Tuple (with one template param).
template <typename Head>
class Tuple<Head> {
public:
  Head value_;

  explicit Tuple(Head value) : value_(value) {}

  template <int n>
  const typename NthType<n, Head>::type&
  get() const {
    return TupleGetHelper<n, Head>::get(*this);
  }
};

void play_with_my_tuple() {
  std::cout << "=== play_with_my_tuple ===" << std::endl;
  Tuple<int, int, int> tuple(1, 2, 3);
  std::cout << "sizeof(tuple) == " << sizeof(tuple) << std::endl;
  std::cout << "0: " << tuple.get<0>() << std::endl;
  std::cout << "1: " << tuple.get<1>() << std::endl;
  std::cout << "2: " << tuple.get<2>() << std::endl;

  // Naturally, this causes a compile error which is not human readable.
  // std::cout << "3: " << tuple.get<3>() << std::endl;
}

int main(int argc, char** argv) {
  play_with_function_template();
  play_with_template_with_value();
  play_with_variadic_template();
  play_with_class_template();
  play_with_my_tuple();
  return 0;
}
