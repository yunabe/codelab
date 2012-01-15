
%{
#include "time.h"
#include "use_time.h"
%}

%typemap(out) yunabe::Time {
  int hour = $1.hour();
  int minute = $1.minute();
  int second = $1.second();
  jclass cls = jenv->FindClass("com/yunabe/time/Time");
  jmethodID cns = jenv->GetMethodID(cls, "<init>", "(III)V");
  $result = jenv->NewObject(cls, cns, hour, minute, second);
}

%typemap(in) yunabe::Time {
  jclass cls = jenv->FindClass("com/yunabe/time/Time");
  jmethodID hourMethod = jenv->GetMethodID(cls, "hour", "()I");
  jmethodID minuteMethod = jenv->GetMethodID(cls, "minute", "()I");
  jmethodID secondMethod = jenv->GetMethodID(cls, "second", "()I");
  int hour = jenv->CallIntMethod($input, hourMethod);
  int minute = jenv->CallIntMethod($input, minuteMethod);
  int second = jenv->CallIntMethod($input, secondMethod);
  $1 = yunabe::Time(hour, minute, second);
}

// wrap.cc. type of jresult.
%typemap(jni) yunabe::Time "jobject"
// TimeModuleJNI.java
%typemap(jtype) yunabe::Time "com.yunabe.time.Time"
// TimeModule.java (both input & output)
%typemap(jstype) yunabe::Time "com.yunabe.time.Time"

%typemap(javain) yunabe::Time "$javainput"
%typemap(javaout) yunabe::Time {
  return $jnicall;
}

namespace yunabe {

yunabe::Time sumTimeAsValue(yunabe::Time x, yunabe::Time y);

}  // namespace yunabe
