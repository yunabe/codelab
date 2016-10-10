// Naing conventions
// https://doc.rust-lang.org/style/style/naming/README.html

use std::mem;


// 1. Variable Bindings
// https://doc.rust-lang.org/book/variable-bindings.html
fn play_with_variables() {
    println!("==== play_play_with_variables ====");
    {
        let x = 3;
        let y: i32 = 4;
        let (a, b) = (7, 8);
        let (c, d): (f32, f64) = (1.2, 3.4);

        // https://doc.rust-lang.org/beta/book/casting-between-types.html#as
        let z: i64 = x + y as i64;
        println!("z == {}", z);
        println!("a + b == {}", a + b);
        println!("c + d == {}", c as f64 + d);
    }
    {
        let x = 3;
        // Error
        // x += 10;

        let mut y = 4;
        y += x;
        println!("y == {}", y);
    }
    {
        let x;
        // Error: Rust does not zero-initialze variables.
        // println!("x == {}", x);
        x = 10;
        println!("x == {}", x);

        // error: re-assignment of immutable variable `x`
        // x = 20;
    }
    {
        let x = 20;
        println!("x == {}", x);
        // Shadowing
        let x = 3.4;
        println!("x == {}", x);

        let mut y = 0;
        y += 1;
        // Make y immutable.
        let y = y;

        // error: re-assignment of immutable variable `y`
        // y += 1;
        println!("y == {}", y);
    }
}

// 2. Functions
// https://doc.rust-lang.org/book/functions.html
fn naive_fib(n: i32) -> i32 {
    if n < 2 {
        return 1;
    }
    return naive_fib(n - 1) + naive_fib(n - 2);
}

fn return_multiple_values() -> (i32, i32) {
    let a = 3;
    return (a, 4);
}

// ! is diverges.
// https://doc.rust-lang.org/book/functions.html#diverging-functions
fn always_panic() -> ! {
    panic!("always_panic should not be called.");
}

fn receive_fn(f: fn(i32) -> i32) {
    let n = 5;
    println!("f({}) = {}", n, f(n));
}

fn play_with_functions(panic: bool) {
    println!("==== play_with_functions ====");
    {
        let n = 15;
        println!("naive_fib({}) = {}", n, naive_fib(n));
    }
    {
        let (a, b) = return_multiple_values();
        println!("a = {}, b = {}", a, b);
    }
    if panic {
        // diverges can be assigned to any type of variables.
        let (x, y): (i32, f32) = always_panic();
        println!("x, y = {}, {}", x, y);
    }
    receive_fn(naive_fib);
}

// 3. Primitive types
// https://doc.rust-lang.org/book/primitive-types.html
fn play_with_primitives() {
    println!("=== play_with_primitives ===");
    {
        // Boaleans
        let b: bool = true;  // or false.
        println!("b is {}", b);
    }
    {
        // char is a single Unicode scalar value.
        let c: char = 'x';
        let multi_c: char = '犬';
        let emoji: char = '😺';
        println!("c: {}, multi_c: {}, emoji: {}", c, multi_c, emoji);
    }
    {
        // Numeric types
        // https://doc.rust-lang.org/book/primitive-types.html#numeric-types

        // signed integers. a and b are overflowing (warning).
        let (a, b, c, d): (i8, i16, i32, i64) = (70000, 70000, 70000, 70000);
        println!("a: {}, b: {}, c: {}, d: {}", a, b, c, d);
        // unsigned integers.
        let (a, b, c, d): (u8, u16, u32, u64) = (70000, 70000, 70000, 70000);
        println!("a: {}, b: {}, c: {}, d: {}", a, b, c, d);

        // isize (signed) and usize (unsigned) depend on the underlying machine architecture.
        let (is, us): (isize, usize) = (2, 3);
        println!("is: {}, us: {}", is, us);
        println!("sizeof(is): {}, sizeof(us): {}",
                 mem::size_of_val(&is),
                 mem::size_of_val(&us));

        let (f0, f1): (f32, f64) = (1.2, 3.4);
        println!("f0: {}, f1: {}", f0, f1);
    }
    {
        // Arrays
        // https://doc.rust-lang.org/book/primitive-types.html#Arrays
        let a = [1, 2, 3];  // a: [i32; 3]
        // initialized array.
        let mut b = [0; 10];  // a: [i32: 10]
        b[1] = 1;
        println!("a: {:?}, b: {:?}", a, b);
        println!("b.len() == {}", b.len());

        // Slices
        {
            let s = &b[1..4];
            println!("s: {:?}, s.len(): {}", s, s.len());
        }
        {
            // the mutable slice type.
            // https://doc.rust-lang.org/std/primitive.slice.html
            // ms can not exist together with s above.
            let ms = &mut b[..];
            ms[0] = 9;
            println!("ms: {:?}, ms.len(): {}", ms, ms.len());
        }
        // `ms[0] = 9` affects to `b`.
        println!("b: {:?}", b);
    }
    {
        // Tuples
        // https://doc.rust-lang.org/book/primitive-types.html#tuples
        let t: (i32, &str) = (42, "Hello");
        println!("t: {:?}", t);
        let (x, y) = t;
        println!("x: {}, y: {}", x, y);
        println!("t.0: {}, t.1: {}", t.0, t.1);

        // single-element tuple
        let single = (8,);
        println!("single: {:?}", single);
    }
}

// 4. Comments
// https://doc.rust-lang.org/book/comments.html

// 5, 6. Flow controls
// if: https://doc.rust-lang.org/book/if.html
// Loops: https://doc.rust-lang.org/book/loops.html
fn play_with_flow_controls() {
    println!("=== play_with_flow_controls ===");
    let n = 10;
    if n % 5 == 0 && n % 3 == 0 {
        println!("Fizz Buzz");
    } else if n % 3 == 0 {
        println!("Fizz");
    } else if n % 5 == 0 {
        println!("Buzz");
    } else {
        println!("{}", n);
    }

    let mut index = 0;
    // infinite-loop.
    loop {
        if index > 5 {
            break;
        }
        println!("in loop : index: {}", index);
        index += 1;
    }
    // while-loop.
    while index < 10 {
        println!("in while: index: {}", index);
        index += 1;
    }
    // for-loop.
    // C-style for is not supported in Rust.
    for index in 10..15 {
        // index = 10, 11, 12, 13, 14.
        // the new variable `index` is defined in this scope.
        println!("index: {}", index);
    }
    println!("in while: index: {}", index);

    // Labeled-break/continue
    'outer: for i in 0..10 {
        for j in 0..10 {
            if i * j > 15 {
                println!("i * j exceeded 15 ({}, {})", i, j);
                break 'outer;
            }
        }
    }
    {
        // In Rust, almost everything is expression.
        // `if` is expression too in Rust.
        let n = 10;
        let a = if n % 2 == 0 { "even" } else { "odd" };
        println!("n is {}", a);

        // if (w/o else), while, loop is evaluated as () (an empty tuple).
        // Personally, I do not like the Rust's philosophy to handle
        // everything as expression so much. It looks just error-prone for me.
        let ifonly_val = if true {
            println!("inside-if!");
        };
        let while_val = while n > 0 {
            println!("inside-while!");
            break;
        };
        let loop_val = loop {
            println!("inside-loop!");
            break;
        };
        println!("ifonly_val: {:?}, while_val: {:?}, loop_val: {:?}",
                 ifonly_val,
                 while_val,
                 loop_val);
    }
}

// 6. Vectors
// https://doc.rust-lang.org/book/vectors.html
fn play_with_vectors() {
    let v = vec![1, 2, 3, 4, 5];
    // zero-initialized.
    let zero = vec![0; 10];
    println!("v = {:?}, zero = {:?}", v, zero);

    let i: i32 = 1;
    let j: isize = i as isize;
    // v[i], v[j] are error. index must be usize.
    // println!("v[i32] = {}, v[isize] = {}", v[i], v[j]);
    let k: usize = j as usize;
    println!("v[{}] = {}", k, v[k]);

    // assignment and push. the vector must be mutable.
    let mut w: Vec<i32> = vec![0; 3];
    w[0] = 1;
    w.push(4);
    println!("w = {:?}", w);

    // Iterating. Without &, for-loop takes the ownsership of v.
    for val in &v {
        println!("v[*]: {}", val);
    }
}

// 8. Ownership
// https://doc.rust-lang.org/book/ownership.html

// The type that does not implement Copy trait is moved
// if it is passed by the argument without &.
fn take_ownership(v: Vec<i32>) {
    println!("took ownership of: {:?}", v);
}

// Returns the ownership to the caller.
fn take_then_return(v: Vec<i32>) -> Vec<i32> {
    println!("took ownership of: {:?}. Then, returning it to the caller.",
             v);
    return v;
}

// Borrow: Simple way to implement take and return the ownership.
fn borrow_ownership(v: &Vec<i32>) {
    println!("borowed ownership of: {:?}", v);
}

fn borrow_mutable(v: &mut Vec<i32>, val: &mut i32) {
    // &mut is a mutable reference.
    // As the pointer in C/C++, &mut can be "dereference"d by *.
    //
    // Note: `mut v: &i32` is different from `v: &mut i32`.
    *v = vec![0; 5];
    v[0] = 1;
    *val = 123;
}

fn play_with_ownership() {
    println!("=== play_with_ownership ===");
    let v = vec![0, 1, 2];
    take_ownership(v);
    // error: use of moved value: `v`
    // println!("v[0]: {}", v[0]);

    let v = vec![3, 4, 5];
    let v = take_then_return(v);  // borrow_ownership(&v);
    // OK
    println!("v after take_then_return: {:?}", v);

    let v = vec![6, 7, 8];
    borrow_ownership(&v);
    // OK
    println!("v after borrow_ownership: {:?}", v);

    let mut v = vec![9, 10, 11];
    let mut val = 0;
    borrow_mutable(&mut v, &mut val);
    println!("v after borrow_mutable: {:?}", v);
    println!("val after borrow_mutable: {:?}", val);
}

fn play_with_structs() {
    println!("play_with_structs");

    // `derive` is required to print the struct with {:?}.
    #[derive(Debug)]
    struct Point {
        x: i32,
        y: i32,
    }
    let origin = Point { x: 0, y: 0 };
    println!("origin: x = {}, y = {}, debug = {:?}",
             origin.x,
             origin.y,
             origin);

    #[derive(Debug)]
    struct PointRef<'a> {
        x: &'a i32,
        y: &'a i32, // z: &i32,  // error: missing lifetime specifier [E0106]
    }
    let (mut a, mut b) = (3, 4);
    {
        let pref = PointRef { x: &a, y: &b };
        println!("pref: {:?}", pref);
        // error: cannot assign to `a` because it is borrowed [E0506]
        // a = 13;
    }
    a = 13;
    b = 14;
    println!("pref1: {:?}", PointRef { x: &a, y: &b });

    // Tuple structs
    struct Color(u8, u8, u8);
    let color = Color(128, 255, 10);
    println!("color: ({}, {}, {})", color.0, color.1, color.2);
    let Color(r, g, b) = color;
    println!("r = {}, g = {}, b = {}", r, g, b);

    // unit-like structs.
    #[derive(Debug)]
    struct Electron {};
    #[derive(Debug)]
    struct Atom;

    let electron = Electron {};  // Electron; is an error.
    let atom = Atom;  // Atom{}; is also fine.
    println!("electron: {:?}, atom: {:?}", electron, atom);
}

// 13. Enums
// https://doc.rust-lang.org/book/enums.html
fn play_with_enums() {
    println!("=== play_with_enums ===");

    #[derive(Debug)]
    enum Message {
        Quit,
        ChangeColor(i32, i32, i32),
        Move { x: i32, y: i32 },
        Write(String),
    }
    let messages = [Message::Quit,
                    Message::ChangeColor(10, 20, 30),
                    Message::Move { x: 100, y: 200 },
                    Message::Write("WriteThis!".to_string())];
    for message in &messages {
        // Note: message: &Message.

        // The enum is like union in C. The size is larger than integers and pointers.
        println!("sizeof(message): {} bytes", mem::size_of_val(message));
        match message {
            &Message::Quit => {
                println!("Quit");
            }
            &Message::ChangeColor(r, g, b) => {
                println!("ChangeColor(r = {}, g = {}, b = {})", r, g, b);
            }
            &Message::Move { x: a, y: b } => {
                // Note: you can get rid of `x: ` and `y: ` if a and b are x and y.
                println!("Move(x: {}, y: {})", a, b);
            }
            &Message::Write(ref s) => {
                println!("Write(s = {})", s);
            }
        }
    }
}

// 15, 16. Pattern Matching
// https://doc.rust-lang.org/book/match.html
// https://doc.rust-lang.org/book/patterns.html
fn play_with_match_and_pattern() {
    println!("==== play_with_match_and_pattern ====");
    let n = 5;
    match n {
        1 => println!("one"),
        2 | 3 => {
            if n == 2 {
                println!("two");
            } else {
                println!("three");
            }
        }
        // Unreachable and detected by the compiler.
        // error: unreachable pattern
        // 3 => {},
        //
        // For ..., the right number is inclusive unlike `..` of for-loop.
        // It looks confusing to me.
        4...9 => println!("from four to nine"),
        // Though this code block is unreachable,
        // the compiler does not detect it.
        3...4 => println!("unreachable but not detected."),
        _ => println!("something else"),
    }
    // match is also expression.
    let s: &str = match n {
        1 => "one",
        2 => "two",
        // Hmm... `,` is optional after {}.
        3 => "three",
        _ => "others",
    };
    println!("n = {}, s = {}", n, s);

    // See play_with_enums for enum match.

    // Patterns.
    let a = 3;
    let b = 4;
    match b {
        // Warning: a here matches to any value (equivalent to _), not to 3.
        // This `a` shadows `a` outside.
        a => println!("in match: a = {}, b = {}", a, b),
    }
    // (a, b) = (3, 4).
    println!("a: {}, b: {}", a, b);

    // Destructuring
    // https://doc.rust-lang.org/book/patterns.html#destructuring
    struct Point {
        x: i32,
        y: i32,
    }
    let point = Point { x: 2, y: 3 };
    // match does not take the ownership of point.
    // I'm not sure how useful this feature is, though.
    match point {
        Point { x, .. } => println!("x is {}", x),
    }
    println!("y is {}", point.y);

    let x = 30;
    match x {
        // Bindings
        // https://doc.rust-lang.org/book/patterns.html#destructuring
        z @ 1...5 => {
            println!("{} is in [1, 5]", z);
        }
        // Guards
        // https://doc.rust-lang.org/book/patterns.html#guards
        z @ 10...20 if z % 2 == 0 => {
            println!("{} is in [10, 20] and even.", z);
        }
        z @ 10 | z @ 20 | z @ 30 | z @ 40 if z > 30 => {
            // 30 is NOT captured by the above pattern because z > 30 is applied to
            // all matches including z @ 30.
            println!("{} matches to the complicated pattern", z);
        }
        _ => {
            println!("uncaptured.");
        }
    }
}

// Method
// https://doc.rust-lang.org/book/method-syntax.html
fn play_with_method() {
    println!("==== play_with_method ====");
    struct Circle {
        x: f64,
        y: f64,
        radius: f64,
    }

    impl Circle {
        fn area(&self) -> f64 {
            std::f64::consts::PI * (self.radius * self.radius)
        }
        fn set_radius(&mut self, r: f64) {
            self.radius = r;
            // error[E0425]: unresolved name `method_noself`
            // You need Circle:: prefix.
            // method_noself(123);
        }
        // Static method.
        fn method_noself(n: i32) {
            println!("method_noself: {}", n);
        }
        fn new_at_orig(radius: f64) -> Circle {
            Circle {
                x: 0.0,
                y: 0.0,
                radius: radius,
            }
        }
    }

    let mut c = Circle {
        x: 0.0,
        y: 1.0,
        radius: 3.0,
    };
    println!("area: {} (radius: {})", c.area(), c.radius);
    c.set_radius(2.0);
    println!("area: {} (radius: {})", c.area(), c.radius);

    // error: no method named `method_noself` found for type `play_with_method::Circle` in the current scope
    // c.method_noself(13);
    Circle::method_noself(13);

    let orig = Circle::new_at_orig(1.0);
    println!("orig.x = {}, orig.y = {}, orig.radius = {}",
             orig.x,
             orig.y,
             orig.radius);
}

// Strings
// https://doc.rust-lang.org/book/strings.html
// - Primitive Type str
// https://doc.rust-lang.org/std/primitive.str.html#method.len
// - Struct std::string::String
// https://doc.rust-lang.org/std/string/struct.String.html
fn play_with_strings() {
    println!("==== play_with_strings ====");
    // The type of string literal is &str.
    let greeting: &str = "Hello there.";
    println!("greeting: {}", greeting);
    let s = "foo\
      bar";
    assert_eq!(s, "foobar");
    let s = "foo
    bar";
    assert_eq!(s, "foo\n    bar");

    // String type.
    let mut s: String = "Hello".to_string();
    s.push_str(" World!");
    println!("s == {}", s.replace("e", "ee"));

    // println!("s[0] = {}", s[0]);

    // Multi-bytes strings.
    let jp = "忠犬ハチ公";
    // len() returns byte-size.
    println!("jp = {}, bytes = {}, num chars: {}",
             jp,
             jp.len(),
             jp.chars().count());

    // error: str, String does not support [index].
    // println!("jp[1] = {}", jp[1]);

    // substring. Though [] is not supported, substring by **byte-offsets** is supported.
    let jpsubstr: &str = &jp[0..6];
    println!("substr = {}", jpsubstr);

    // Runtime crash: index 0 and/or 7 in `忠犬ハチ公` do not lie on character boundary
    // println!("substr = {}", &jp[0..7]);

    // Other operations:
    // Concat.
    let hello = "Hello ".to_string();
    let world = "World";
    let helloworld = hello + world;
    println!("helloworld = {}", helloworld);

    // `Deref` coercions
    let hello = "Hello ".to_string();
    let h0: &String = &hello;
    // `Deref` coercions
    // https://doc.rust-lang.org/book/deref-coercions.html
    let h1: &str = &hello;
    println!("h0 = {}, h1 = {}", h0, h1);
}

fn play_with_generics() {
    println!("==== play_with_generics ====");
    enum MyOption<T> {
        MySome(T),
        MyNone,
    }
    // Note: You can not omit MyOptions:: prefix.
    let x: MyOption<i32> = MyOption::MySome(5);
    // You can not omit MyOption:: here either.
    match x {
        MyOption::MySome(n) => {
            println!("x: value = {}", n);
        }
        MyOption::MyNone => {}
    }

    // Result
    // https://doc.rust-lang.org/std/result/enum.Result.html
    // Is there any way to infer theses types?
    let ok: Result<i32, &str> = Result::Ok(3);
    let err: Result<i32, &str> = Result::Err("error");
    match ok {
        Result::Ok(val) => {
            println!("ok (ok): {}", val);
        }
        Result::Err(err) => {
            println!("ok (error): {}", err);
        }
    }

    // Generics function.
    // std::ops::Add trait is necessary to use `+` operator.
    // https://doc.rust-lang.org/std/ops/trait.Add.html
    fn sum<T: std::ops::Add>(x: T, y: T) -> <T as std::ops::Add>::Output {
        return x + y;
    }
    println!("sum(3, 4) = {}", sum(3, 4));
}

// Traits
// https://doc.rust-lang.org/book/traits.html
//
// Trait is something like Java/Go interface on C++ template.
// Everything is resolved statically (at compile time).
fn play_with_traits() {
    println!("==== play_with_traits ====");

    trait HasArea {
        fn area(&self) -> f64;
    }

    struct Circle {
        x: f64,
        y: f64,
        radius: f64,
    }

    impl HasArea for Circle {
        fn area(&self) -> f64 {
            std::f64::consts::PI * (self.radius * self.radius)
        }
    }

    fn print_area<T: HasArea>(x: &T) {
        println!("x.area == {}", x.area());
    }
    // You can also use `where` to add the trait restriction.
    // https://doc.rust-lang.org/book/traits.html#where-clause
    // It's readable than the previous way when there are a lot of args.
    // I'm not sure it's good idea to have two different ways to
    // write the same thing in one language, though.
    fn print_area_with_where<T>(x: &T)
        where T: HasArea
    {
        println!("x.area (with where) == {}", x.area());
    }

    let c = Circle {
        x: 0.0,
        y: 0.0,
        radius: 2.0,
    };
    print_area(&c);
    print_area_with_where(&c);
    println!("c.area == {}", c.area());

    // Method name conflict
    trait SayHello {
        fn hello(&self);
    }
    trait AnotherSayHello {
        fn hello(&self, name: &str);
    }

    struct HelloWorld;

    impl SayHello for HelloWorld {
        fn hello(&self) {
            println!("Hello World!");
        }
    }
    impl AnotherSayHello for HelloWorld {
        fn hello(&self, name: &str) {
            println!("Hello {}!", name);
        }
    }
    let h = HelloWorld;
    // error[E0034]: multiple applicable items in scope
    // h.hello();

    // Cast to traits to call the conflicted method.
    // Note: you can not omit `&` because SayHello is "unsized type".
    // TODO: Confirm this involves dynamic-dispatch and `vtable` lookup.
    (&h as &SayHello).hello();
    (&h as &AnotherSayHello).hello("Rust");

    // https://doc.rust-lang.org/book/traits.html#trait-bounds-on-generic-structs
    // It is possible to implement
    struct Rect<T> {
        x: T,
        y: T,
        width: T,
        height: T,
    }
    // In other words, T support == operator.
    impl<T: PartialEq> Rect<T> {
        fn is_square(&self) -> bool {
            self.width == self.height
        }
    }

    let r = Rect {
        x: 0,
        y: 0,
        width: 10,
        height: 10,
    };
    assert!(r.is_square());

    #[derive(Debug)]
    struct MyType;

    let rs = Rect {
        x: MyType,
        y: MyType,
        width: MyType,
        height: MyType,
    };
    println!("rs.x: {:?}, rs.y: {:?}", rs.x, rs.y);
    // error: no method named `is_square` found for type.
    // assert!(rs.is_square());

    // More complicated pattern.
    // trait with generics with trait!
    trait GenericHasArea<T: std::ops::Mul> {
        fn area(&self) -> <T as std::ops::Mul>::Output;
    }
    impl<T: std::ops::Mul + Copy> GenericHasArea<T> for Rect<T> {
        fn area(&self) -> <T as std::ops::Mul>::Output {
            self.width * self.height
        }
    }
    println!("r.area(): {}", r.area());
    // error: no method named `area` found for type ...
    // println!("rs.area(): {}", rs.area());

    // Trait with default methods
    // https://doc.rust-lang.org/book/traits.html#default-methods
    trait WithDefault {
        fn is_valid(&self) -> bool;
        fn is_invalid(&self) -> bool {
            !self.is_valid()
        }
    }
    struct StructWithDefault;
    impl WithDefault for StructWithDefault {
        fn is_valid(&self) -> bool {
            return false;
        }
    }

    let swd = StructWithDefault;
    println!("swd.is_invalid(): {}", swd.is_invalid());

    struct HasDrop {
        id: i32,
    }
    impl Drop for HasDrop {
        fn drop(&mut self) {
            println!("Dropping: {}", self.id);
        }
    }
    {
        let d = HasDrop { id: 0 };
        let moved = d;
        let moved = 3;
        // drop is executed immediately! What?
        let _ = HasDrop { id: 1 };
        println!("Before drop.");
        // Drop with `0` is called after this.
    }
}

// https://doc.rust-lang.org/book/if-let.html
fn play_with_iflet() {
    println!("==== play_with_iflet ====");
    let mut opt = Option::Some(3);
    if let Some(val) = opt {
        println!("if-let: {}", val);
    }
    while let Some(val) = opt {
        println!("while-let: {}", val);
        if val > 0 {
            opt = Option::Some(val - 1);
        } else {
            opt = Option::None;
        }
    }
}

// Trait Objects.
// https://doc.rust-lang.org/book/trait-objects.html
// Trait can also behave as Java/Go interface.
fn play_with_trait_objects() {
    println!("==== play_with_trait_objects ====");
    // Dynamic dispatch
    trait SayHello {
        fn hello(&self);
    }
    struct Hello {
        name: String,
    }
    impl SayHello for Hello {
        fn hello(&self) {
            println!("Hello {}", self.name);
        }
    }

    fn static_dispatch_hello<H: SayHello>(h: &H) {
        println!("static_dispatch_hello...");
        h.hello();
    }
    // Trait Objects!
    // https://doc.rust-lang.org/book/trait-objects.html#representation
    fn dynamic_dispatch_hello(h: &Hello) {
        println!("dynamic_dispatch_hello...");
        h.hello();
    }

    let h = Hello { name: "Rust".to_string() };
    static_dispatch_hello(&h);

    dynamic_dispatch_hello(&h as &Hello);
    // coercing. It's equivalent to the above one.
    dynamic_dispatch_hello(&h);

    // Object Safety
    // https://doc.rust-lang.org/stable/book/trait-objects.html#object-safety
    // TODO: Understand this part well.
    //
    // trait Sized:
    // https://doc.rust-lang.org/std/marker/trait.Sized.html
    trait MySized: Sized {}

    // error: the trait `Fuga` cannot be made into an object.
    // note: the trait cannot require that `Self : Sized`
    // fn hello(m: &MySized) {}
}

fn play_with_closures() {
    println!("==== play_with_closures ====");
    {
        // basic syntax.
        let plus_one = |x: i32| x + 1;
        assert_eq!(4, plus_one(3));
        // It's not very different from fn.
        fn plus_one_fn(x: i32) -> i32 {
            x + 1
        }
        assert_eq!(4, plus_one_fn(3));
    }
    {
        // borrow variables from the environment.
        let mut num = 5;
        num += 1;
        let plus_num = |x: i32| x + num;
        // error: cannot assign to `num` because it is borrowed
        // num += 1;
        assert_eq!(8, plus_num(2));
    }
    {
        // borrow mutable variables from the environment.
        let mut num = 0;
        {
            let mut assign_num = |x: i32| {
                num = x;
            };  // Do not omit this `;`
            assign_num(10);
            // error: cannot borrow `num` as immutable because it is also borrowed as mutable
            // assert_eq!(10, num);
        }
        assert_eq!(10, num);
    }
    {
        println!("-- move closure --");
        let mut num = 0;
        struct Movable {
            x: i32,
        }
        let m0: Movable = Movable { x: 10 };
        let m1: Movable = Movable { x: 20 };

        // The `move` closure captures the environment by move semantic.
        // - num is copied because it satisfis Copy trait.
        // - m0 is moved.
        // - m1 is not moved because it's not accessed from the closure.
        let mut move_closure = move |expected_num: i32| {
            assert_eq!(expected_num, num);
            num += 1;
            println!("m0.x = {}", m0.x);
        };
        // error: use of moved value: `m0.x`
        // println!("m0.x = {}", m0.x);
        println!("m1.x = {}", m1.x);

        // It does not affect to num inside the closure because it was copied.
        num = 100;
        // This increments `num` inside the closure. But it does not affect to
        // the original num.
        move_closure(0);
        move_closure(1);
        // num is not incremented by move_closure.
        assert_eq!(100, num);
    }
    {
        // closure implements Fn traits.
        let sum = |x: i32, y: i32| x + y;
        fn static_dispatch<F: Fn(i32, i32) -> i32>(f: &F) {
            println!("static: f(3, 4) = {}", f(3, 4));
        }
        static_dispatch(&sum);
        fn dynamic_dispatch(f: &Fn(i32, i32) -> i32) {
            println!("dynamic: f(3, 4) = {}", f(3, 4));
        }
        dynamic_dispatch(&sum);

        // A function pointer.
        fn sum_fn(x: i32, y: i32) -> i32 {
            x + y
        }
        static_dispatch(&sum_fn);
        dynamic_dispatch(&sum_fn);
    }
    {
        // TODO: Understand 'static after F.
        fn apply_twice<T, F: 'static>(f: F) -> Box<Fn(T) -> T>
            where F: Fn(T) -> T
        {
            println!("sizeof(F) = {}", mem::size_of_val(&f));
            return Box::new(move |x| f(f(x)));
        }
        {
            let twice = apply_twice(|x: i32| x * 2);
            println!("twice(3): {}", twice(3));
            let num = 5;
            let twice = apply_twice(move |x: i32| x + num);
            println!("twice(3): {}", twice(3));
        }
        {
            let n = 10;
            let add_n = |x: i32| {
                return x + n;
            };
            println!("add_n(5) = {}", add_n(5));
            // Because of `F: 'static,` all borrows in F should be 'static lifetime.
            // error: closure may outlive the current function, but it borrows `n`, which is owned by the current function
            // let twice = apply_twice(add_n);
        }
    }
}

fn play_with_lifetime() {
    println!("==== play_with_lifetime ====");
    {
        fn identify_expl<'a>(x: &'a i32) -> &'a i32 {
            x
        }
        // identify_impl is equivalent of identify_expl.
        // Rust compiler assumes that the lifetime of the return value
        // is the same as the arg.
        fn identify_impl(x: &i32) -> &i32 {
            x
        }
        {
            let mut m = 0;
            // The borrowed reference &m is released immediately in this case.
            println!("m = {}", identify_expl(&m));
            m += 1;
            // &m is not released immediately, because it has the same lifetime as r.
            let r = identify_expl(&m);
            // Thus, we can not modify m here because the reference of m is borrowd by r.
            // error: cannot assign to `m` because it is borrowed
            // m += 1;
            println!("r = {}", r);
        }
        {
            // Double check the behavior of identify_impl.
            let mut m = 0;
            println!("m = {}", identify_impl(&m));
            m += 1;
            let r = identify_impl(&m);
            // error: cannot assign to `m` because it is borrowed
            // m += 1;
            println!("r = {}", r);
        }

        // The case where we need to specify explicit lifetimes.
        fn select_first<'a, 'b>(x: &'a i32, y: &'b i32) -> &'a i32 {
            x
        }
        // error: missing lifetime specifier
        // We need to specify the life time of the return value is same as
        // &x or &y. Rust compiler does not infer it from the function body.
        //
        // fn select_first_impl(x: &i32, y: &i32) -> &i32 {
        //    x
        // }
        {
            let (mut m, mut n) = (10, 20);
            let r = select_first(&m, &n);
            n += 1;
            // error: cannot assign to `m` because it is borrowed
            // m += 1;
            println!("m = {}, n = {}, r = {}", m, n, r);
        }
    }
    {
        // struct and lifetime.
        struct SimpleStruct {
            x: i32,
        }
        impl SimpleStruct {
            // The lifetime of the return value of the method is same as
            // the lifetime of &self.
            fn get_x_ref(&self) -> &i32 {
                return &self.x;
            }
            // You can not omit 'a.
            fn identify<'a>(&self, n: &'a i32) -> &'a i32 {
                return n;
            }
            // The lifetime of the return value is same as (or narrower than)
            // the lifetime of self and or.
            fn get_x_ref_or<'a>(&'a self, or: &'a i32) -> &'a i32 {
                if self.x >= 0 {&self.x} else {&or}
            }
        }
    }
}

fn play_with_smart_pointers() {
    println!("==== play_with_smart_pointers ====");
    {
        // Box is the unique pointer in Rust.
        #[derive(Debug)]
        struct Disposable;
        impl Drop for Disposable {
            fn drop(&mut self) {
                println!("Drop Disposal");
            }
        }
        let d = Box::new(Disposable);
        println!("d = {:?}", d);
    }
}

fn main() {
    play_with_variables();
    play_with_functions(false);
    play_with_primitives();
    play_with_flow_controls();
    play_with_vectors();
    play_with_ownership();
    play_with_structs();
    play_with_enums();
    play_with_match_and_pattern();
    play_with_method();
    play_with_strings();
    play_with_generics();
    play_with_traits();
    play_with_iflet();
    play_with_trait_objects();
    play_with_closures();
    play_with_lifetime();
    play_with_smart_pointers();
}
