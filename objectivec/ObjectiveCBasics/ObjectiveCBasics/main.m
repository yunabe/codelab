//
//  main.m
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/26.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "YNBPerson.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        YNBPerson* person = [YNBPerson personWithName:@"Taro" birtyday: [NSDate dateWithTimeIntervalSince1970:0]];
        NSLog(@"person == %@", [person description]);
        NSLog(@"person.age == %ld", person.age);
    }
    return 0;
}
