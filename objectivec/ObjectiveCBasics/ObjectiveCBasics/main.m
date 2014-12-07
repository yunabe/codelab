//
//  main.m
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/26.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "YNBPerson.h"
#import "YNBEmployee.h"
#import "YNBPerson+YNBPersonAgeAdditions.h"

void ObjectBasic() {
    YNBPerson* person = [YNBPerson personWithName:@"Taro" birthday: [NSDate dateWithTimeIntervalSince1970:0]];
    NSLog(@"person == %@", [person description]);
    NSLog(@"person.age == %ld", person.age);

    YNBEmployee* emp = [[YNBEmployee alloc] initWithName:@"Jiro" birtyday:[NSDate dateWithTimeIntervalSince1970:86400 * 365 * 10] salary:72.5];
    NSLog(@"emp == %@", emp);
    NSLog(@"emp.salary == %.2f", emp.salary);
    NSLog(@"emp.age == %ld", emp.age);

    // Defined in category.
    NSLog(@"emp.ageInDays == %ld", emp.ageInDays);
}

void LearnObjectLifeCycle();
void LearnProtocol();

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        ObjectBasic();
        LearnObjectLifeCycle();
        LearnProtocol();
    }
    return 0;
}
