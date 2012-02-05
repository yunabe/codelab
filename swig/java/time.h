#ifndef YUNABE_TIME_H_
#define YUNABE_TIME_H_

#include <string>

namespace yunabe {

class Time {
 public:
  Time();
  Time(int hour, int minute, int second);

  int hour() const;
  int minute() const;
  int second() const;
  std::string ToString() const;

 private:
  // not const to allow assignment.
  int second_;
};

}  // namespace

#endif  // YUNABE_TIME_H_
