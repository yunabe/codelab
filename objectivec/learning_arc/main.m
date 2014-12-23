#import <Foundation/Foundation.h>

@interface YNBObj : NSObject
@property NSString* name;
@end

@implementation YNBObj
- (instancetype)initWithName:(NSString*)name {
  self = [super init];
  if (self) {
    self.name = name;
  }
  return self;
}

- (void)dealloc {
  NSLog(@"YNBObj (%@) is released.", self.name);
}
@end

int main(int argc, char** argv) {
  @autoreleasepool {
    NSArray* array0 = [NSArray arrayWithObjects:[[YNBObj alloc] initWithName:@"arrayWith"], nil];
    NSArray* array1 = [[NSArray alloc] initWithObjects:[[YNBObj alloc] initWithName:@"initWith"], nil];
    array0 = nil;
    array1 = nil;
    NSLog(@"end of autoreleasepool");
  }
  return 0;
}
