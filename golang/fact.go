package main

import "fmt"

func fact(n int) int {
  if n > 1 {
    return n * fact(n - 1)
  }
  return 1
}

func play_with_array() {
	fmt.Println("### play_with_array ###")
	var a [3]int  // all set to 0
	fmt.Println(a)
	fmt.Printf("a[0] == %d\n", a[0])
	fmt.Printf("len(a) == %d\n", len(a))

	// Array literals
	a  = [3]int{1, 2, 3}
	fmt.Println(a)
	a  = [...]int{4, 5, 6}
	fmt.Println(a)
	a  = [3]int{0:7, 2:8}
	fmt.Println(a)

	// Type error:
	// cannot use array literal (type [4]int)
	// as type [3]int in assignment
	// a = [4]int{1, 2, 3, 4}
}

func play_with_slice() {
	var array [10]int;
	array[0] = 0
	array[1] = 1
	array[2] = 2

	// slice
	var slice []int
	slice = array[:]
	fmt.Printf("len(slice) = %d\n", len(slice))
	fmt.Printf("cap(slice) = %d\n", cap(slice))
	fmt.Printf("slice[0] = %d\n", slice[0])
	slice = array[1:]
	fmt.Printf("len(slice) = %d\n", len(slice))
	fmt.Printf("cap(slice) = %d\n", cap(slice))
	fmt.Printf("slice[0] = %d\n", slice[0])

	// slice literal
	slice = []int{1, 3, 5}
	fmt.Println(slice)

	// alloc arbitrary size array to slice
	slice = make([]int, 20)
	fmt.Printf("len(slice) == %d\n", len(slice))
	fmt.Printf("cap(slice) == %d\n", cap(slice))

	slice = array[3:5]
	fmt.Printf("len(slice) == %d\n", len(slice))
	fmt.Printf("cap(slice) == %d\n", cap(slice))

	slice = make([]int, 10, 20)
	fmt.Printf("len(slice) == %d\n", len(slice))
	fmt.Printf("cap(slice) == %d\n", cap(slice))
	// fmt.Println(slice[15])  // index out of range
	slice = slice[:20]
	fmt.Printf("slice[15] = %d\n", slice[15])
	// slice = slice[:100]  // index out of range
}

func play_with_pointer() {
	fmt.Println("### play_with_pointer ###")
	var x int = 1
	var p *int = &x
	fmt.Printf("*p == %d\n", *p)
	x = 2
	fmt.Printf("*p == %d\n", *p)
	p = nil
	fmt.Println(p)
}

func main() {
  n := 5
  fmt.Printf("fact(%d) = %d\n", n, fact(n))
  play_with_array()
	play_with_slice()
	play_with_pointer()
}
