package main

import (
	"bufio"
	"fmt"
	"net"

	"goprotobuf.googlecode.com/hg/proto"
)

func HandleConnection(conn *net.UnixConn) {
	defer conn.Close()
	defer fmt.Println("closing...")
	r := bufio.NewReader(conn)
	w := bufio.NewWriter(conn)

	req, err := ReceiveRequest(r)
	if req != nil {
		fmt.Println("req.Name =", *req.Name)
		res := new(Response)
		res.Name = proto.String("hello hello!")
		SendResponse(w, res)
		w.Flush()
	} else {
		fmt.Println("Failed to receive a request:", err)
	}
}

func main() {
	laddr := net.UnixAddr{Net: "unix", Name: "/tmp/sock"}
	listener, err := net.ListenUnix("unix", &laddr)
	if err != nil {
		fmt.Println("Err:", err)
		return
	}
	defer listener.Close()
	for {
		c, _ := listener.AcceptUnix()
		fmt.Println("accepted...")
		go HandleConnection(c)
	}
}
