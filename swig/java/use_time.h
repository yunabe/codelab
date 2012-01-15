#ifndef YUNABE_USE_TIME_H_
#define YUNABE_USE_TIME_H_

#include "time.h"

namespace yunabe {

Time sumTimeAsValue(Time x, Time y);
void sumTimeAsReference(const Time& x, const Time& y, Time* out);

}  // namespace yunabe

#endif  // YUNABE_USE_TIME_H_
