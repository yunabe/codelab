//  LearnValuesCollections.m

#import <Foundation/Foundation.h>

void LearnValuesCollections() {
    // In Objective-C, use BOOL rather than bool (C99).
    // Literals of BOOL are YES and NO.
    // BOOl is signed char (See objc.h).
    BOOL b = YES;
    NSLog(@"b == %d", b);

    // Foundation Data Types Reference
    // https://developer.apple.com/library/ios/documentation/Cocoa/Reference/Foundation/Miscellaneous/Foundation_DataTypes/index.html
    // NSInteger is long (typedef long NSInteger).
    NSInteger nsint = 13;
    NSLog(@"nsint == %ld", nsint);
    
    // NSRange is structure... initialize/stringify by static methods.
    NSRange range = NSMakeRange(40, 60);
    NSLog(@"range == %@", NSStringFromRange(range));
    
    // NSNumber is a wrapper object for primitive types.
    // https://developer.apple.com/library/ios/documentation/Cocoa/Reference/Foundation/Classes/NSNumber_Class/index.html
    NSNumber* num = [NSNumber numberWithInteger:nsint];
    NSLog(@"num == %@", [num stringValue]);
    NSLog(@"num:type == %s (@encode(NSString) == %s)", [num objCType], @encode(long));
    
    // NSValue is a wrapper for NS* structures (e.g. NSRange)
    // NSValue is the parent of NSNumber...
    // https://developer.apple.com/library/ios/documentation/Cocoa/Reference/Foundation/Classes/NSValue_Class/index.html
    NSValue* val = [NSValue valueWithRange:range];
    NSLog(@"val:type == %s (@encode(NSRange) == %s)", [val objCType], @encode(NSRange));
    // IMPORTANT! Do not use == to compare objCType and @encode.

    ////////////////////////////
    ////  Collections  /////////
    ////////////////////////////
    
    // TODO: Read
    // https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/Collections/Collections.html
    
    //////// NSArray //////////
    // array literal and primitive type literals.
    NSArray* array0 = @[@10, @(-4), @3.14, @YES];
    NSLog(@"array0 length: %ld", [array0 count]);
    
    
    // for-in statement.
    // Be careful. Not type-safety.
    for (NSNumber* obj in array0) {
        NSLog(@"obj == %@", obj.stringValue);
    }
    // reverse enumerator
    for (NSNumber* val in [array0 reverseObjectEnumerator]){
        NSLog(@"reverse: val == %@", val.stringValue);
    }
    
    // Another way to initialize NSArray.
    NSArray* array1 = [NSArray arrayWithObjects:@10, @20, @30, nil];
    NSLog(@"array1 length: %ld", [array1 count]);
    
    NSArray* arrayWithNull = @[@1, @2, [NSNull null], @5];
    for (id val in arrayWithNull) {
        // NSNull detection.
        if (val == [NSNull null]) {
            NSLog(@"arrayWithNull: val was null...");
        } else {
            NSLog(@"arrayWithNull: val == %@", val);
        }
    }
    
    NSMutableArray* mutableArray = [NSMutableArray arrayWithObjects:@"apple", @"banana", @"curry", nil];
    NSLog(@"mutableArray[0] == %@", mutableArray[0]);
    // mutableArray[1] = nil; <-- NSInvalidArgumentException
    // You must not set nil to Objective-C collections.
    mutableArray[1] = [NSNull null];
    for (id val in mutableArray) {
        NSLog(@"mutableArray: val == %@", val);
    }
    
    ///////// NSSet /////////
    // Values for NSSet and keys for NSDictionary must implement "hash" and "isEqual".
    NSSet* set = [NSSet setWithObjects:@20, @10, @30, @20, nil];
    NSLog(@"set length: %ld", [set count]);
    for (NSNumber* val in set) {
        NSLog(@"set:val == %@", val.stringValue);
    }
    
    ///////// NSDictionary ////
    NSDictionary* dict = @{
      @"a": @"apple",
      @"b": @"banana",
      };
    
    // A error. NSDictionary is read-only. Use NSMutableDictionary (a child class of NSMutable).
    // dict[@"c"] = "curry";

    NSLog(@"dict[\"a\"] == %@", dict[@"a"]);
    // nil is returned when the key is not contained.
    NSLog(@"dict[\"unknown\"] == %@", [dict valueForKey:@"unknown"]);

    // for-each
    for (NSString* key in dict) {
        NSLog(@"dict[%@] == %@", key, [dict valueForKey:key]);
    }

    // Another way to initialize NSDictionary. The order of key, value is reversed...
    NSDictionary* dict1 = [NSDictionary dictionaryWithObjectsAndKeys: @"capcake", @"c", @"donuts", @"d", nil];
    for (NSString* key in dict1) {
        NSLog(@"dict1[%@] == %@", key, [dict1 valueForKey:key]);
    }
    
    // mutable NSDictionary.
    // Note: Even if a dictionary is empty, you can not initialize a dictionary only with "alloc".
    NSMutableDictionary* mutableDict = [NSMutableDictionary dictionaryWithObjectsAndKeys:nil];
    mutableDict[@"d"] = @"dog";
    for (NSString* key in mutableDict) {
        NSLog(@"mutableDicct[%@] == %@", key, [mutableDict valueForKey:key]);
    }
}
