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
	d = Data{y:10, string:"hoge", x:10}
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
	return math.Sqrt(p.x * p.x + p.y * p.y)
}

func play_with_method() {
	fmt.Println("### play_with_method ###")
	p := Point{3, 4}
	fmt.Printf("p.Abs() == %f\n", p.Abs())
}

func main() {
	play_with_struct()
	play_with_method()
}
