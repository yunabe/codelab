// The code to understand how to replace an method of an instance
// dynamically in ObjC.
//
// clang -framework Foundation -fobjc-arc -Wall dynamic_class_def.m -o dynamic_class_def && ./dynamic_class_def

#import <Foundation/Foundation.h>
#include <objc/runtime.h> 

@interface YNBParent : NSObject
- (void)doSomething;
@end

@implementation YNBParent
- (void)doSomething {
  NSLog(@"doSomething in YNBParent.");
}
@end

@interface YNBDummyParent : NSObject
- (void)doSomething;
@end

@implementation YNBDummyParent
- (void)doSomething {
  NSLog(@"doSomething in YNBDummyParent.");
}
@end

@interface YNBDummy : YNBDummyParent
- (void)doSomethingDummy;
- (void)doSomethingOriginal;
@end

@implementation YNBDummy
- (void)doSomethingDummy {
  [super doSomething]; // doSomething in YNBDummyParent.
  [self doSomethingOriginal];  // doSomething in YNBParent!
  NSLog(@"doSomethingDummy in YNBDummy.");
}
- (void)doSomethingOriginal {
  NSLog(@"Should not be called.");
}
@end

int main(int argc, char** argv) {
  @autoreleasepool {
    YNBParent* p = [YNBParent alloc];

    Class newClass = objc_allocateClassPair(p.class, [@"YNBDynamicChild" cStringUsingEncoding:NSASCIIStringEncoding], 0);
    Method method = class_getInstanceMethod([YNBDummy class], @selector(doSomethingDummy));
    class_addMethod(newClass, @selector(doSomething), method_getImplementation(method), method_getTypeEncoding(method));

    Method original = class_getInstanceMethod(p.class, @selector(doSomething));
    class_addMethod(newClass, @selector(doSomethingOriginal), method_getImplementation(original), method_getTypeEncoding(original));

    objc_registerClassPair(newClass);
    object_setClass(p, newClass);

    [p doSomething];
  }
  return 0;
}
