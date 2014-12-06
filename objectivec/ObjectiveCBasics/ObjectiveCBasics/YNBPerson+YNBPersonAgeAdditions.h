//  An example of "category".
//  https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/CustomizingExistingClasses/CustomizingExistingClasses.html

#import "YNBPerson.h"

// "Category"
// "category" is similar to "class extension".
// But you can not define "variables" in "category"!
// (Thus, default property implementation is not generated in "category".)
//
// TODO: Understand why.
@interface YNBPerson (YNBPersonAgeAdditions)
@property (readonly) NSInteger ageInDays;
- (NSInteger) ageInDaysAt: (NSDate*) at;
@end
