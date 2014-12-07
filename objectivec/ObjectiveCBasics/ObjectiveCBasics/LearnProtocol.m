// Working with Protocols
// https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingwithProtocols/WorkingwithProtocols.html


#import <Foundation/Foundation.h>

@protocol YNBProtocolA
@property (readonly) NSString* propA;  // It's possible to declare property in protocol (but it's unusual?)
- (void) someMethodA: (int) arg;
@end

@protocol YNBProtocolB
- (void) someMethodB: (double) arg;
@end

@protocol YNBProtocolC <YNBProtocolA, YNBProtocolB>
@end

@interface YNBImplementation : NSObject<YNBProtocolC>
// You don't need to declare methods in protocol explicitly here.
@end

@implementation YNBImplementation

- (NSString *)propA {
    return @"YNBImplementation:propA";
}

- (void)someMethodA:(int)arg {
    NSLog(@"YNBImplementation.someMethodA is invoked: %d", arg);
}

- (void)someMethodB:(double)arg {
    NSLog(@"YNBImplementation.someMethodB is invoked: %f", arg);
}

@end

// The pointer to an instance that inherits a protocol is "id<ProtocolName>" rather than ProtocolName*.
void RecieveProtocol(id<YNBProtocolC> proto) {
    [proto someMethodA:123];
    [proto someMethodB:3.14];
}

// Although it's very confusing, it's okay to conflict protocol name and interface name...
// (e.g. NSObject.h defines @interface NSObject and @protocol NSObject....)
@protocol SameName
- (void) sameName;
@end

@interface SameName : NSObject<SameName>
@end

@implementation SameName
- (void)sameName {
    NSLog(@"sameName method in @interface SameName that implements @protocol SameName.");
}
@end

void LearnProtocol() {
    RecieveProtocol([YNBImplementation alloc]);
    
    // SameName is @interface SameName...
    SameName* sn = [SameName alloc];
    // SameName is @protocol SameName...
    id<SameName> isn = sn;
    [isn sameName];
}
