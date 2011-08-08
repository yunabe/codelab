all: fact func

fact: fact.8
	8l -o fact fact.8

fact.8: fact.go
	8g fact.go

func: func.8
	8l -o func func.8

func.8: func.go
	8g func.go

clean:
	rm -rf *.8 fact func
