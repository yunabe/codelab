package main

import "fmt"

func simple(x int, y int) int {
	return x + y
}

func swap(x int, y int) (int, int) {
	return y, x
}

func play_with_basic_func() {
	fmt.Println("### play_with_func ###")
	fmt.Println("simple(3, 4) ==", simple(3, 4))
	x, y := swap(3, 4)
	fmt.Printf("swap(3, 4) == %d, %d\n", x, y)
	z, _ := swap(1, 7)
	fmt.Println("z ==", z)
}

func play_with_closure() {
	fmt.Println("### play_with_closure ###")
	var x = 0
	tmp := func() {
		x = 1
	}
	tmp()
	fmt.Println("x ==", x)
}

func play_with_defer() {
	// I feel using in C# is simpler and easy to use...
	for i := 0; i < 3; i++ {
		defer fmt.Printf("simple defer: %d\n", i)
		defer func(){fmt.Printf("defer with closure: %d\n", i)}()
	}
}

func main() {
	play_with_basic_func()
	play_with_closure()
	play_with_defer()
}
