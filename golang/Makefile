all: fact func oop

fact: fact.8
	8l -o fact fact.8

fact.8: fact.go
	8g fact.go

func: func.8
	8l -o func func.8

func.8: func.go
	8g func.go

oop: oop.8
	8l -o oop oop.8

oop.8: oop.go
	8g oop.go

clean:
	rm -rf *.8 fact func oop
