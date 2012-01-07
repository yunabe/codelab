package main

import (
	"fmt"
	"io"
	"net/http"
	"log"
	"time"
	"websocket"
)

const response string = `
<html>
  <script>
    var ws = null;

    function sendMessage() {
      var input = document.getElementById('input').value;
      if (!input) {
        return;
      }
      document.getElementById('input').value = '';
      ws.send(input);
    }

function init() {
  var url = window.location.href.match(/^\w+:\/\/[^\/]+\//)[0];
  url = url.replace(/^\w+:/, 'ws:') + 'ws';
  ws = new WebSocket(url);
  ws.onmessage = onmessage;
  ws.onopen = onopen;
  ws.onclose = onclose;
}

function addMessage(message) {
  var out = document.getElementById('output');
  output.innerHTML = output.innerHTML + '<br>' + message;
}

function onopen(e) {
  addMessage('A web socket connection was opened.');
}

function onclose(e) {
  addMessage('A web socket connection was closed.');
}

function onmessage(e) {
  addMessage('Recieved: ' + e.data);
}
  </script>
  <body onload="init()">
    <form>
      <input type="text" id="input"></input>
      <input type="button" value="send" onclick="sendMessage()"></input>
    </form>
    <div id="output"></div>
  </body>
</html>`

func HtmlResponseServer(w http.ResponseWriter, req *http.Request) {
	fmt.Println("HtmlResponseServer")
	io.WriteString(w, response);
}

func NotFoundServer(w http.ResponseWriter, req *http.Request) {
	fmt.Println("Not found:", req.URL.String())
	w.WriteHeader(404)
	io.WriteString(w, "Not found\n")
}

func WebSocketServer(ws *websocket.Conn) {
	fmt.Println("WebSocketServer")
	var msg [1024]byte;
	ch := CreateReadChannel(ws, msg[:])
	interval := time.Tick(5 * 1e9)
Loop: for {
		select {
		case n := <- ch:
			if n == 0 {
				fmt.Println("The connection was closed by peer.")
				break Loop
			}
			ws.Write(msg[:n])
		case _ = <- interval:
			ws.Write([]byte("An interval event fired in a server side."))
		}
	}
}

func CreateReadChannel(ws *websocket.Conn, msg []byte) chan int {
	ch := make(chan int)
	go ReadThread(ws, msg, ch)
	return ch
}

func ReadThread(ws *websocket.Conn, msg []byte, ch chan int) {
	for {
		n, error := ws.Read(msg)
		if error != nil {
			fmt.Println("WebSocket read error: ", error)
			ch <- 0
			break
		}
		ch <- n
		if n == 0 {
			break
		}
	}
}

func main() {
	http.HandleFunc("/", NotFoundServer)
	http.HandleFunc("/test", HtmlResponseServer)
	http.Handle("/ws", websocket.Handler(WebSocketServer))
	err := http.ListenAndServe(":8888", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
