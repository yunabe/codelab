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

func channnel_and_deadlock(casenum int) {
	switch casenum {
	case 0:
		ich := make(chan int)
		ich <- 0

	case 1:
		ich := make(chan int)

		go func() {
			// Deadlock occurs if you forget to close a channel.
			// defer close(ich)
			for i := 1; i < 5; i++ {
				ich <- i * i
			}
		}()

		for num := range ich {
			fmt.Println("num =", num)
		}

	case 2:
		// Starvation
		ch0 := make(chan int, 1)
		ch1 := make(chan int, 1)
		done := make(chan bool, 2)

		go func() {
			// No starvation if read and write are swapped.
			fmt.Println("Recieved from ch1:", <- ch1)
			ch0 <- 0
			done <- true
		}()
		go func() {
			fmt.Println("Recieved from ch0:", <- ch0)
			ch1 <- 1
			done <- true
		}()

		// Wait
		<- done
		<- done
	}

}

func main() {
	play_with_channel()
	// channnel_and_deadlock(2)
}
