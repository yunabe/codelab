//
//  ObjectLifeCycle.m
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/27.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface YNBMyObj : NSObject
@property NSString* name;
@property YNBMyObj* strongRef;
@end

@implementation YNBMyObj
- (instancetype)initWithName:(NSString*)name {
    self = [super init];
    if (self) {
        _name = name;
    }
    return self;
}

- (void)dealloc {
    NSLog(@"dealloc: %@", [self name]);
}

@end

void LearnObjectLifeCycle() {
    NSLog(@"########## LearnObjectLifeCycle #############");
    
    YNBMyObj* a = [[YNBMyObj alloc] initWithName:@"a"];
    YNBMyObj* b = [[YNBMyObj alloc] initWithName:@"b"];
    NSLog(@"reset a...");  // a is dealloced here.
    a = nil;
    b.strongRef = [[YNBMyObj alloc] initWithName:@"c"];
    // b.strongRef.strongRef = b;  // cyclic ref. Memory Leak!
    NSLog(@"############# end ################");
}