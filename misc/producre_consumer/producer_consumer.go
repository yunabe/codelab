// Go version of Producer/Consumer pattern is 10x+ faster than C/C++/Java thread versions.

package main

import (
	"fmt"
)

func Produce(w chan<- int) {
	defer close(w)
	for i := 0; i < 1000 * 1000; i++ {
		w <- i
	}
}

func Consume(r <-chan int, finish chan<- bool) {
	defer close(finish)
	for {
		i, ok := <- r
		if !ok {
			break
		}
		if i % (100 * 1000) == 0 {
			fmt.Println("i ==", i)
		}
	}
}

func main() {
	ch := make(chan int)
	finish := make(chan bool)
	go Produce(ch)
	go Consume(ch, finish)
	<-finish
}
