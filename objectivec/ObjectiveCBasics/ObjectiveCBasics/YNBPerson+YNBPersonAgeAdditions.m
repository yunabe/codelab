//
//  YNBPerson+YNBPersonAgeAdditions.m
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/29.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import "YNBPerson+YNBPersonAgeAdditions.h"

@implementation YNBPerson (YNBPersonAgeAdditions)

// In "category", you must define property accessors because default accessors are not defined implicitly.
- (NSInteger)ageInDays {
    return [self ageInDaysAt:[NSDate dateWithTimeIntervalSinceNow:0]];
}

- (NSInteger) ageInDaysAt: (NSDate*) at {
    // NSDate* now =
    NSCalendar *calendar = [NSCalendar currentCalendar];
    NSDate *fromDate;
    NSDate *toDate;
    [calendar rangeOfUnit:NSCalendarUnitDay startDate:&fromDate
                 interval:NULL forDate:self.birthday];
    [calendar rangeOfUnit:NSCalendarUnitDay startDate:&toDate
                 interval:NULL forDate:at];

    NSDateComponents *difference = [calendar components:NSCalendarUnitDay
                                               fromDate:fromDate toDate:toDate options:0];

    return [difference day];
}

// Sprisingly, you can override methods of the original class...
// Don't do write such code... the behavior is undefined...
// c.f. "Avoid Category Method Name Clashes" in
// https://developer.apple.com/library/mac/documentation/cocoa/conceptual/ProgrammingWithObjectiveC/CustomizingExistingClasses/CustomizingExistingClasses.html
- (void)dealloc {
    NSLog(@"YNBPerson dealloc defined in YNBPerson. Don't write such code!");
}
@end
