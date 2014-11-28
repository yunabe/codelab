//
//  ObjectLifeCycle.m
//  ObjectiveCBasics
//
//  Created by yunabe on 2014/11/27.
//  Copyright (c) 2014年 yunabe. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface YNBMyObj : NSObject {
    YNBMyObj* strongRefVar;  // __string is declared implicitly.
    YNBMyObj* __weak weakRefVar;
}

@property NSString* name;
@property YNBMyObj* strongRefProp;  // (string) is declared implicitly.
@property (weak) YNBMyObj* weakRefProp;

- (void) setStrongRefVar:(YNBMyObj *)ref;
- (YNBMyObj *)strongRefVar;
- (void) setWeakRefVar:(YNBMyObj *)ref;
- (YNBMyObj*) weakRefVar;

@end

@implementation YNBMyObj
- (instancetype)initWithName:(NSString*)name {
    self = [super init];
    if (self) {
        _name = name;
    }
    return self;
}

- (NSString *)description {
    return [NSString stringWithFormat:@"<myobj: %@>", self.name];
}

- (void)dealloc {
    NSLog(@"dealloc: %@", [self name]);
}

- (void) setStrongRefVar:(YNBMyObj *)ref {
    strongRefVar = ref;
}

- (YNBMyObj *)strongRefVar {
    return weakRefVar;
}

- (void) setWeakRefVar:(YNBMyObj *)ref {
    weakRefVar = ref;
}

- (YNBMyObj *)weakRefVar {
    return weakRefVar;
}

@end

void LearnObjectLifeCycle() {
    // Objects are managed by reference counting.
    NSLog(@"########## begin: LearnObjectLifeCycle #############");
    YNBMyObj* a = [[YNBMyObj alloc] initWithName:@"a"];
    YNBMyObj* b = [[YNBMyObj alloc] initWithName:@"b"];
    NSLog(@"reset a...");  // a is dealloced here.
    a = nil;
    NSLog(@"Set strong ref to b.");
    b.strongRefProp = [[YNBMyObj alloc] initWithName:@"c"];
    NSLog(@"reset b...");  // a is dealloced here.
    b = nil;  // b and c are deallocated.
    
    YNBMyObj* d = [[YNBMyObj alloc] initWithName:@"d"];
    YNBMyObj* e = [[YNBMyObj alloc] initWithName:@"e"];
    d.weakRefProp = e;
    NSLog(@"d.weakRefProp == %@", d.weakRefProp);  // d.weakRef is e.
    NSLog(@"Reset e");
    e = nil;  // e is deallocated because d.weakRef is a weak reference.
    NSLog(@"d.weakRefProp == %@", d.weakRefProp);  // d.weakRef is nil.
    d = nil;
    
    YNBMyObj* f = [[YNBMyObj alloc] initWithName:@"f"];
    YNBMyObj* g = [[YNBMyObj alloc] initWithName:@"g"];
    [f setStrongRefVar:g];
    NSLog(@"reset g");
    g = nil;
    NSLog(@"reset f");
    f = nil;
    
    YNBMyObj* h = [[YNBMyObj alloc] initWithName:@"h"];
    YNBMyObj* i = [[YNBMyObj alloc] initWithName:@"i"];
    [h setWeakRefVar:i];
    NSLog(@"h.weakRefVar == %@", h.weakRefVar);  // h.weakRef is i.
    NSLog(@"Reset i");
    i = nil;  // g is deallocated because g is held by a __weak variable.
    NSLog(@"h.weakRefVar == %@", h.weakRefVar);  // h.weakRef is nil.
    NSLog(@"############# end: LearnObjectLifeCycle ################");
    
    // TODO: Learn __unsafe_unretained.
}
