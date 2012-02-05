#ifndef YUNABE_USE_TIME_H_
#define YUNABE_USE_TIME_H_

#include "time.h"

namespace yunabe {

Time sumTimeAsValue(Time x, Time y);
void sumTimeAsReference(const Time& x, const Time& y, Time* out);

class Subtractor {
 public:
  Subtractor();
  virtual ~Subtractor();
  virtual Time subtract(Time x, Time y);
};

Time subtractTime(Time x, Time y);

void registerSubtractor(Subtractor *subtractor);

}  // namespace yunabe

#endif  // YUNABE_USE_TIME_H_
