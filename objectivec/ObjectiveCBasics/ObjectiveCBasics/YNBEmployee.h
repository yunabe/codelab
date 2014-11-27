//
//  YNBEmployee.h
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/27.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import "YNBPerson.h"

@interface YNBEmployee : YNBPerson
@property double salary;
- (id) initWithName:(NSString *)first birtyday:(NSDate *)birthday salary:(double) salary;
@end
