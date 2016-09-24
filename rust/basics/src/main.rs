// Naing conventions
// https://doc.rust-lang.org/style/style/naming/README.html

// 1. Variable Bindings
// https://doc.rust-lang.org/book/variable-bindings.html
fn play_with_variable() {
    {
        let x = 3;
        let y: i32 = 4;
        let (a, b) = (7, 8);

        // https://doc.rust-lang.org/beta/book/casting-between-types.html#as
        let z: i64 = x + y as i64;
        println!("z == {}", z);
        println!("a + b == {}", a + b);
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

fn main() {
    play_with_variable();
}
