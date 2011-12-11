#include <jni.h>
#include <stdio.h>
#include <pthread.h>

bool CreateJVM(JavaVM** jvm, JNIEnv** env) {
  JavaVMOption options[3];
  options[0].optionString = "-Xmx128m";
  JavaVMInitArgs vm_args;
  vm_args.version = JNI_VERSION_1_6;
  vm_args.options = options;
  vm_args.nOptions = 1;
  return JNI_CreateJavaVM(jvm, (void**)env, &vm_args) == JNI_OK;
}

void CallCalcSum(JNIEnv* env, int x, int y) {
  jclass cls = env->FindClass("Calc");
  if (cls == NULL) {
    printf("Failed to find Calc.\n");
  }
  jmethodID mid = env->GetStaticMethodID(cls, "sum", "(II)I");
  if (mid == NULL) {
    printf("Failed to find sum in Calc.\n");
  }
  jint result = env->CallStaticIntMethod(cls, mid, x, y);
  printf("Calc.sum(%d, %d) == %d\n", x, y, result);
}

struct CallCalcSumArg {
  JavaVM* jvm;
  JNIEnv* env;
  int x;
  int y;
};

void* CallCalcSumInThread(void* void_arg) {
  CallCalcSumArg* arg = (CallCalcSumArg*)void_arg;
  JNIEnv* env;
  // ** Bad example **
  printf("'env' created in the main thread is not available "
         "in another therad. It will cause segmentation fault.\n");
  env = arg->env;
  CallCalcSum(env, arg->x, arg->y);

  // ** How to fix? **
  // arg->jvm->AttachCurrentThread((void**)&env, NULL);
  // CallCalcSum(env, arg->x, arg->y);
  // arg->jvm->DetachCurrentThread();
}

void ReuseEnvInDifferentThread() {
  printf("== Begin ReuseEnvInDifferentThread ==\n");
  JavaVM* jvm;
  JNIEnv* env;
  if (!CreateJVM(&jvm, &env)) {
    printf("Failed to create JVM, unexpectedly.\n");
    return;
  }
  printf("First, call Java codes from C++ in the main thread.\n");
  CallCalcSum(env, 3, 4);

  CallCalcSumArg arg;
  arg.jvm = jvm;
  arg.env = env;
  arg.x = 7;
  arg.y = 8;

  pthread_t th;
  printf("Then, call Java codes in a different thread.\n");
  pthread_create(&th, NULL, &CallCalcSumInThread, &arg);
  pthread_join(th, NULL);
}

int main(int argc, char** argv) {
  ReuseEnvInDifferentThread();
  return 0;
}
