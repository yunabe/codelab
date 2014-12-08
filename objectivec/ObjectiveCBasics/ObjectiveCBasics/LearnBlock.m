// https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingwithBlocks/WorkingwithBlocks.html

#import <Foundation/Foundation.h>


// TODO: Understand why this is not working...
// NSArray* NotWorking() {
//   __block int counter = 0;
//   return [NSArray arrayWithObjects: ^(){
//     NSLog(@"---- 0 ----");
// }, ^(){
//     NSLog(@"---- 1 ---- (%d)", counter);
//   }, nil];
// }

typedef void (^YNBSimpleBlock)(void);

// repeat, block are optional (like a function forward declaration.)
typedef void(^YNBBlockRepeater)(int repeat, YNBSimpleBlock block);

// * typedef improves the readability of code drastically.
//   void FuncWithBlock(void(^repeater)(int, void(^)(void))) {
void FuncWithBlock(YNBBlockRepeater repeater) {
  repeater(5, ^{
    NSLog(@"FuncWithBlock!");
  });
}

void LearnBlock() {
   void (^simpleBlock)(void) = ^{  // (void) can be ().
    NSLog(@"This is a block");
  };
  simpleBlock();
  
  double (^blockWithArgs)(int, int) = ^ double (int x, int y){
    return 1.0 * x / y;
  };
  // You can get rid of "return type" from block literals.
  // (return type is defined implicitly from the body of the block.
  //  Thus, a compile error if you replace the first int with double).
  int (^square)(int) = ^(int n) {
    return n * n;
  };
  NSLog(@"blockWithArgs(3, 4) = %.3f", blockWithArgs(3, 4));
  NSLog(@"square(6) == %d", square(6));
  
  int outerVal = 1;
  __block int blockOuterVal = 10;
  void (^printOuterVal)() = ^{
    NSLog(@"outerVal == %d", outerVal);
    NSLog(@"blockOuterVal == %d", blockOuterVal);
  };
  printOuterVal();// outerVal == 1 and blockOuterVal == 10.
  outerVal = 2;  // It does not affect to outerVal in printOuterVal.
  blockOuterVal = 20;  // It affects to blockOuterVal in printOuterVal!
  printOuterVal();  // outerVal == 1 and blockOuterVal == 20.

  NSLog(@"&outerVal: %p", &outerVal);  // In stack
  // In heap because __block variables are managed with GC.
  // https://developer.apple.com/library/ios/documentation/Cocoa/Conceptual/Blocks/Articles/bxVariables.html#//apple_ref/doc/uid/TP40007502-CH6-SW6
  NSLog(@"&blockOuterVal: %p", &blockOuterVal);

  // NSArray* ar = NotWorking();
  // void(^ar0)() = ar[0];
  // ar0();
  
  FuncWithBlock(^(int repeat, YNBSimpleBlock block) {
    for (int i = 0; i < repeat; ++i) {
      NSLog(@"Run block (i == %d)", i);
      block();
    }
  });
}
