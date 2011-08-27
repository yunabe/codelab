all: basic func oop concurrency websocket

basic: basic.8
	8l -o basic basic.8

basic.8: basic.go
	8g basic.go

func: func.8
	8l -o func func.8

func.8: func.go
	8g func.go

oop: oop.8
	8l -o oop oop.8

oop.8: oop.go
	8g oop.go

concurrency: concurrency.8
	8l -o concurrency concurrency.8

concurrency.8: concurrency.go
	8g concurrency.go

websocket: websocket.8
	8l -o websocket websocket.8

websocket.8: websocket.go
	8g websocket.go

clean:
	rm -rf *.8 basic func oop concurrency websocket
