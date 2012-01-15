#include "time.h"

#include <stdio.h>

using std::string;

namespace yunabe {

Time::Time() : second_(0) {}

Time::Time(int hour, int minute, int second)
  : second_(hour * 3600 + minute * 60 + second) {}

int Time::hour() const {
  return second_ / (60 * 60);
}

int Time::minute() const {
  return (second_ / 60) % 60;
}

int Time::second() const {
  return second_ % 60;
}

string Time::ToString() const {
  static char buf[100];
  snprintf(buf, 100, "%02d:%02d:%02d", hour(), minute(), second());
  return string(buf);
}

}  // namespace
