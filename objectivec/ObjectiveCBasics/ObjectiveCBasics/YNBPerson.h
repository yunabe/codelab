//
//  YNBPerson.h
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/26.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

// You don't need
// #ifndef ObjectiveCBasics_YNBPerson_h
// #define ObjectiveCBasics_YNBPerson_h
// ...
// #endif
// macro because "#import" makes sure that the same file is never included more than once.

#import <Foundation/Foundation.h>

// 3 chars prefix was required as convention.
// https://developer.apple.com/library/mac/documentation/cocoa/conceptual/ProgrammingWithObjectiveC/Conventions/Conventions.html#//apple_ref/doc/uid/TP40011210-CH10-SW2
@interface YNBPerson : NSObject

@property NSString* name;
@property (readonly) NSDate* birthday;

// TODO: Understand why initXX returns "id" rather than (YNBPerson*) in Objective-C.
- (id) initWithName: (NSString*)first birthday: (NSDate*)birthday;
- (NSInteger) age;
- (NSInteger) ageAt: (NSDate*) at;

+ (YNBPerson*) personWithName: (NSString*)first birthday: (NSDate*)birthday;
@end

