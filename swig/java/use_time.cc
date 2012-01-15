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

}  // namespace yunabe
