//
//  YNBPerson.m
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/26.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import "YNBPerson.h"

@implementation YNBPerson {
    // instance variables are zero-initialized.
    NSInteger age;  // NSIntger == long.
}

// Rename the instant variable implicitly defined by @property.
@synthesize birthday = internalBirthday;

- (id) initWithName: (NSString*)name birthday: (NSDate*)birthday {
    // See "Access Instance Variables Directly from Initializer Methods" in
    // https://developer.apple.com/library/mac/documentation/cocoa/conceptual/ProgrammingWithObjectiveC/EncapsulatingData/EncapsulatingData.html#//apple_ref/doc/uid/TP40011210-CH5-SW1
    self = [super init];
    if (self) {
        _name = name;  // or self.name = name;
        internalBirthday = birthday;
        age = -1;
    }
    return self;
}

// description is "toString" in Objective-C.
- (NSString *)description {
    // self.name is a syntax sugar of [self name];
    return [NSString stringWithFormat:@"<Name: %@, Birthday: %@>", self.name, [self birthday]];
}

// "Compiler" does not show any warning if you forget to define this :{
- (NSInteger)age {
    return [self ageAt:[NSDate dateWithTimeIntervalSinceNow:0]];
}

- (NSInteger)ageAt:(NSDate *)at {
    if (age >= 0) {
        return age;
    }
    NSCalendar* cal = [[NSCalendar alloc] initWithCalendarIdentifier:NSCalendarIdentifierGregorian];
    NSDateComponents *components = [cal components:NSCalendarUnitYear fromDate:self.birthday toDate:at options:0];
    age = components.year;
    return age;
}

+ (YNBPerson *)personWithName:(NSString *)first birthday:(NSDate *)birthday {
    return [[YNBPerson alloc] initWithName:first birthday:birthday];
}

@end
