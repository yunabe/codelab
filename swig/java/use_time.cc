#include <stdio.h>

#include "time.h"
#include "use_time.h"

namespace yunabe {

Time sumTimeAsValue(Time x, Time y) {
  return Time(x.hour() + y.hour(),
              x.minute() + y.minute(),
              x.second() + y.second());
}

void sumTimeAsReference(const Time& x, const Time& y, Time* out) {
  *out = Time(x.hour() + y.hour(),
              x.minute() + y.minute(),
              x.second() + y.second());
}

static Subtractor* registeredSubtractor = NULL;

Subtractor::Subtractor() {
}

Subtractor::~Subtractor() {
}

Time Subtractor::subtract(Time x, Time y) {
  return Time(0, 0, 0);
}

Time subtractTime(Time x, Time y) {
  printf(" C++: Calling registered subtractor.\n");
  Time result = registeredSubtractor->subtract(x, y);
  printf(" C++: Result is %s\n", result.ToString().c_str());
  return result;
}
  
void registerSubtractor(Subtractor *subtractor) {
  registeredSubtractor = subtractor;
}

}  // namespace yunabe
