//
//  YNBPerson.m
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/26.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import "YNBPerson.h"

// "class extension" overrides class declarations.
// By class extension, you can
// * define "private" properties.
// * override definitoins of properties.
//   (e.g. readonly -> readwrite: adds a "private" default setter method.)
// * define "private" methods (methods that are ).
//
// Note:
// "private" means "not visible" from other files at "compile" time because
// mothds/properties are not declared in public .h file.
// At runtime, no difference between properties/methods in the header file and those in the class extension
@interface YNBPerson ()
- (NSInteger)ageAtInternal:(NSDate *)at;
@end

@implementation YNBPerson {
    // - instance variables are zero-initialized.
    // - {} here is optional.
    // - You can move this to .h file.
    //   But instance variable are not visible even if they are defined in .h.
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
    age = [self ageAtInternal:at];
    return age;
}

- (NSInteger)ageAtInternal:(NSDate *)at {
    NSCalendar* cal = [[NSCalendar alloc] initWithCalendarIdentifier:NSCalendarIdentifierGregorian];
    NSDateComponents *components = [cal components:NSCalendarUnitYear fromDate:self.birthday toDate:at options:0];
    return components.year;
}

+ (YNBPerson *)personWithName:(NSString *)first birthday:(NSDate *)birthday {
    return [[YNBPerson alloc] initWithName:first birthday:birthday];
}

@end
