package main

import (
	"fmt";
	"time"
)

func child_routine(n int, ch chan bool) {
	time.Sleep(1e9)
	if n >= 0 {
		fmt.Println("child_routine: OK")
		ch <- true
	} else {
		fmt.Println("child_routine: Error")
		ch <- false
	}
}

func channel_as_return_value(loop int) chan string {
	ch := make(chan string)
	go func() {
		for i := 0; i < loop; i++ {
			time.Sleep(0.2e9)
			ch <- fmt.Sprintf("A message from a go routine: %d", i)
		}
		close(ch)
	}()
	return ch
}

func channel_of_channnel() chan chan string {
	var result chan chan string = make(chan chan string, 2)
	defer close(result)

	ch0 := make(chan string)
	result <- ch0
	ch1 := make(chan string)
	result <- ch1

	go func() {
		defer close(ch0)
		for i := 0; i < 5; i++ {
			ch0 <- fmt.Sprintf("ch0: %d", i)
		}
	}()
	go func() {
		defer close(ch1)
		for i := 0; i < 5; i++ {
			ch1 <- fmt.Sprintf("ch1: %d", i)
		}
	}()
	return result
}

func play_with_channel() {
	fmt.Println("### play_with_channel ###")
	ch := make(chan bool)
	go child_routine(10, ch)
	fmt.Println("Waiting for the child routine")

	// "if <- ch {" is also allowed.
	if ok := <- ch; ok {
		fmt.Println("Parent: OK")
	} else {
		fmt.Println("Parent: Error")
	}

	var sch chan string
	sch = channel_as_return_value(5)
	for {
		message, ok := <- sch
		if !ok {
			fmt.Println("The channel was closed.")
			break
		}
		fmt.Printf("Recieved with for  : %s\n", message)
	}

	sch = channel_as_return_value(5)
	for message := range sch {
		fmt.Printf("Recieved with range: %s\n", message)
	}

	cc := channel_of_channnel()
	for sch = range cc {
		for message := range sch {
			fmt.Println(message)
		}
	}
}

func main() {
	play_with_channel()
}
