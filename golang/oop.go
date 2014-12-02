package main

import (
	"fmt"
	"math"
)

type MyInt int

type Data struct {
	x int
	y int
	string
}

type MoreData struct {
	Data
	z int
}

func play_with_struct() {
	fmt.Println("### play_with_struct ###")
	var d Data
	d.x = 3
	d.y = 4
	d.string = "hoge"
	fmt.Printf("d.x, d.y, d.string == %d, %d, %s\n",
		d.x, d.y, d.string)

	var pd *Data = new(Data)
	pd.x = 7
	pd.y = 8
	pd.string = "piyo"
	fmt.Printf("pd.x, pd.y, pd.string == %d, %d, %s\n",
		pd.x, pd.y, pd.string)

	// without "type"
	var a struct {
		field string
	}
	a.field = "hello"
	fmt.Println("a.field ==", a.field)

	// Initialization
	d = Data{}
	d = Data{10, 20, "hoge"}
	d = Data{y: 10, string: "hoge", x: 10}
	pd = &Data{10, 20, "hoge"}

	// An anonymous struct field
	md := MoreData{}
	md.x = 10
	md.y = 20
	md.string = "piyoo"
	fmt.Printf("md.x, md.y, md.string == %d, %d, %s\n",
		md.x, md.y, md.string)
	fmt.Println("md.Data ==", md.Data)

	// Initialization of struct with an anonymous struct field
	md = MoreData{Data{1, 2, "foo"}, 3}
}

type Point struct {
	x float64
	y float64
}

func (p *Point) Abs() float64 {
	return math.Sqrt(p.x*p.x + p.y*p.y)
}

func play_with_method() {
	fmt.Println("### play_with_method ###")
	p := Point{3, 4}
	fmt.Printf("p.Abs() == %f\n", p.Abs())
}

type AbsInterface interface {
	Abs() float64
}

// Checkes whehter *Point implements AbsInterface.
// http://golang.org/doc/effective_go.html#blank_implements
var _ AbsInterface = (*Point)(nil)

type Point2 struct {
	x float64
	y float64
}

func (p Point2) Abs() float64 {
	return math.Sqrt(p.x*p.x + p.y*p.y)
}

// Either struct and pointer works as AbsInterface
// when struct is receiver (though it's unusual).
// If the receiver is pointer (e.g. Point), struct does not work as AbsInterface.
var _ AbsInterface = Point2{0, 0}
var _ AbsInterface = (*Point2)(nil)

func play_with_interface() {
	fmt.Println("### play_with_interface ###")
	var ai AbsInterface
	p := Point{3, 4}
	ai = &p
	fmt.Println(ai)
	ai = nil
	fmt.Println(ai == nil) // true
	ai = (*Point2)(nil)
	// BE CAREFUL!
	// https://golang.org/doc/faq#nil_error
	fmt.Println(ai == nil) // false
	p2 := Point2{3, 4}
	ai = p2
	p2.x = 100
	fmt.Println(ai)
}

type FooInterface interface {
	Foo()
}

type BarInterface interface {
	Bar()
}

type FooBar struct {
}

// Not func Foo (*FooBar) ()...
func (*FooBar) Foo() {
}

func (*FooBar) Bar() {
}

func play_with_type_assertion() {
	fmt.Println("### play_with_type_assertion ###")
	var any interface{}
	any = int(100)

	x := any.(int)
	// x := any.(float64)  // runtime error
	fmt.Println("x =", x)

	// No runtime error
	if f, ok := any.(float64); ok {
		fmt.Println(f, ok)
	}

	// type switch
	switch t := any.(type) {
	case int:
		// t is "int" here
		var z int = t
		fmt.Println("int:", z)
	case string:
		// t is "string" here
		var s string = t
		fmt.Println("string:", s)
	default:
		// t is interface {} here
		fmt.Println("others:", t)
	}

	foobar := &FooBar{}
	foo := FooInterface(foobar)
	bar := foo.(BarInterface) // It is allowed.
	fmt.Println("bar (foobar) =", bar)
}

func main() {
	play_with_struct()
	play_with_method()
	play_with_interface()
	play_with_type_assertion()
}
