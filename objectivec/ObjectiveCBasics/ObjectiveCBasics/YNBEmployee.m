//
//  YNBEmployee.m
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/27.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import "YNBEmployee.h"

@implementation YNBEmployee

- (id)initWithName:(NSString *)first birtyday:(NSDate *)birthday salary:(double)salary {
    self = [super initWithName:first birthday:birthday];
    if (self) {
        self.salary = salary;
    }
    return self;
}

// In Objective-C, initialization methods are inherited in child classes.
// So, we need to override all initialization methods on an parent class...Hmm...?
// TODO: Any solution?
-(id)initWithName:(NSString *)first birthday:(NSDate *)birthday {
    return [self initWithName:first birtyday:birthday salary:50.0];
}
@end
