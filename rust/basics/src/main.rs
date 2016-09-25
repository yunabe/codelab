// Naing conventions
// https://doc.rust-lang.org/style/style/naming/README.html

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
fn always_panic(n: i32) -> ! {
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
        let (x, y): (i32, f32) = always_panic(10);
        println!("x, y = {}, {}", x, y);
    }
    receive_fn(naive_fib);
}

// 3. Primitive types
// https://doc.rust-lang.org/book/primitive-types.html
fn play_with_primitives() {
    println!("=== play_with_primitives ===");
}

fn main() {
    play_with_variables();
    play_with_functions(false);
    play_with_primitives();
}
