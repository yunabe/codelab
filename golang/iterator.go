package main

import "fmt"
import "time"

const loopEnd = 10 * 1000 * 1000

// channel

func newRangeChannel() <-chan int {
	ch := make(chan int)
	go func() {
    defer close(ch)
    for i := 0; i < loopEnd; i++ {
			ch <- i
		}
  }()
	return ch
}
 
func channelVersionMain() {
	start := time.Now()
	for _ = range newRangeChannel() {}
	elapsed := time.Since(start)
	fmt.Println("Channel Version:", elapsed)
}

// next method

func nextInt(i *int) bool {
	*i++
	return *i < loopEnd
}

func nextVersionMain() {
	start := time.Now()
	i := -1
	for nextInt(&i) {}
	elapsed := time.Since(start)
	fmt.Println("Next version:", elapsed)
}

// closure

func iterateIntRange(body func(int) bool) {
	for i := 0; i < loopEnd; i++ {
		if !body(i) {
			break
		}
	}
}

func closureVersionMain() {
	start := time.Now()
	iterateIntRange(func(i int) bool {
		return true
	})
	elapsed := time.Since(start)
	fmt.Println("Closure version:", elapsed)
}
 
func main() {
	channelVersionMain()
	nextVersionMain()
	closureVersionMain()
}
