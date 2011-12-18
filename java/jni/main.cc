#include <jni.h>
#include <stdio.h>

int main(int argc, char** argv) {
  JNIEnv* env;
  JavaVM* jvm;
  JavaVMOption options[3];
  options[0].optionString = "-Xmx128m";
  JavaVMInitArgs vm_args;
  vm_args.version = JNI_VERSION_1_6;
  vm_args.options = options;
  vm_args.nOptions = 1;
  jint ret = JNI_CreateJavaVM(&jvm, (void**)&env, &vm_args);
  if (ret != JNI_OK) {
    printf("Failed to create JVM.\n");
    return 1;
  }
  jclass cls = env->FindClass("Calc");
  if (cls == NULL) {
    printf("Failed to find Calc.\n");
  }
  jmethodID mid = env->GetStaticMethodID(cls, "sum", "(II)I");
  if (mid == NULL) {
    printf("Failed to find sum.\n");
  }
  int x = 6;
  int y = 13;
  jint result = env->CallStaticIntMethod(cls, mid, x, y);
  printf("Calc.sum(%d, %d) == %d\n", x, y, result);

  mid = env->GetStaticMethodID(cls, "throw_exception", "()V");
  if (mid == NULL) {
    printf("Failed to find throw_exception.\n");
  }
  env->CallStaticVoidMethod(cls, mid);
  jthrowable exception = env->ExceptionOccurred();
  if (exception != NULL) {
    env->ExceptionDescribe();  // Clear is called implicitly?
    printf("Exception occurred.\n");
    env->ExceptionClear();
  }

  cls = env->FindClass("Data");
  if (cls == NULL) {
    printf("Failed to find Data.\n");
    return 1;
  }
  // ';'!
  mid = env->GetStaticMethodID(cls, "create", "(I)LData;");
  if (mid == NULL) {
    printf("Failed to find create.\n");
    return 1;
  }    
  for (int i = 0; i < 1000; ++i) {
    // Memory leak if PushLocalFrame ans PopLocalFrame are not called.
    env->PushLocalFrame(10);
    env->CallStaticObjectMethod(cls, mid, 1000 * 1000);
    jthrowable exception = env->ExceptionOccurred();
    if (exception != NULL) {
      env->ExceptionDescribe();
      env->ExceptionClear();
      break;
    }
    env->PopLocalFrame(NULL);
  }
  return 0;
}
