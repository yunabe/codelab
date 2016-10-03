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
}
