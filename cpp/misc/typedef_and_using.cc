// g++ typedef_and_using.cc -std=c++11 -o typedef_and_using && ./typedef_and_using

#include <vector>
#include <iostream>

namespace yunabe {

  typedef int MyInt;
  // New typedef format in C++11.
  using MyFloat = float;

  // In namespace yunabe, you can get rid of std:: before cout and endl.
  using std::cout;
  using std::endl;

  // using and typedef with template instantiations.
  using IntVec = std::vector<int>;
  typedef std::vector<float> FloatVec;

  // using can be used with template. typedef can not.
  template <typename T> using Vec = std::vector<T>;

}  // namespace yunabe

namespace yunabe {
  void Subroutine() {
    // types defined in the previous section.
    MyInt myi = 43;
    MyFloat myf = 4.3;
    IntVec iv = {1, 2, 3};
    FloatVec fv = {1.1, 2.2, 3.3};
    Vec<char> vc = {'a', 'b', 'c'};
    // You do not need std:: before cout and endl.
    cout << "=== Subroutine ===" << endl;
    cout << "myi: " << myi << endl;
    cout << "myf: " << myf << endl;
    cout << "iv: " << iv[0] << endl;
    cout << "fv: " << fv[0] << endl;
    cout << "vc: " << vc[0] << endl;
  }
}

int main(int argc, char** argv) {
  // You can access types defined in namespace yunabe with yunabe::.
  yunabe::MyInt myi = 10;
  // You need std:: here.
  std::cout << "myi: " << myi << std::endl;

  yunabe::Subroutine();
  return 0;
}
