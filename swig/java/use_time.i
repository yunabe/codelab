%module(directors="1") modulename

%feature("director") Subtractor;

%{
#include "time.h"
#include "use_time.h"
%}

%define TIME_CPP2JAVA(cppvar, javavar)
{
  int hour = cppvar.hour();
  int minute = cppvar.minute();
  int second = cppvar.second();
  jclass cls = jenv->FindClass("com/yunabe/time/Time");
  jmethodID cns = jenv->GetMethodID(cls, "<init>", "(III)V");
  javavar = jenv->NewObject(cls, cns, hour, minute, second);
}
%enddef

%define TIME_JAVA2CPP(javavar, cppvar)
{
  jclass cls = jenv->FindClass("com/yunabe/time/Time");
  jmethodID hourMethod = jenv->GetMethodID(cls, "hour", "()I");
  jmethodID minuteMethod = jenv->GetMethodID(cls, "minute", "()I");
  jmethodID secondMethod = jenv->GetMethodID(cls, "second", "()I");
  int hour = jenv->CallIntMethod(javavar, hourMethod);
  int minute = jenv->CallIntMethod(javavar, minuteMethod);
  int second = jenv->CallIntMethod(javavar, secondMethod);
  cppvar = yunabe::Time(hour, minute, second);
}
%enddef

%typemap(out) yunabe::Time TIME_CPP2JAVA($1, $result)

%typemap(in) yunabe::Time TIME_JAVA2CPP($input, $1)

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

// no descriptor causes segv of swig.
%typemap(directorin,descriptor="Lcom/yunabe/time/Time;") yunabe::Time TIME_CPP2JAVA($1, $input)

%typemap(directorout) yunabe::Time TIME_JAVA2CPP($input, $1)

// $jniinput can be $javainput or $1.
%typemap(javadirectorin) yunabe::Time "$jniinput"
%typemap(javadirectorout) yunabe::Time "$javacall"

namespace yunabe {

yunabe::Time sumTimeAsValue(yunabe::Time x, yunabe::Time y);

class Subtractor {
 public:
  virtual ~Subtractor();
  virtual yunabe::Time subtract(yunabe::Time x, yunabe::Time y);
};

yunabe::Time subtractTime(yunabe::Time x, yunabe::Time y);
void registerSubtractor(Subtractor *subtractor);

}  // namespace yunabe
