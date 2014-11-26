//
//  YNBPerson.h
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/26.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface YNBPerson : NSObject
@property NSString* name;
@property (readonly) NSDate* birthday;

// TODO: Understand why initXX returns "id" rather than (YNBPerson*) in Objective-C.
- (id) initWithName: (NSString*)first birtyday: (NSDate*)birthday;
- (NSInteger) age;
- (NSInteger) ageAt: (NSDate*) at;

+ (YNBPerson*) personWithName: (NSString*)first birtyday: (NSDate*)birthday;
@end
