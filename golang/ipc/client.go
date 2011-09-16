package main

import (
	"fmt"
	"bufio"
	"net"

	"goprotobuf.googlecode.com/hg/proto"
)

func main() {
	laddr := net.UnixAddr{Net: "unix", Name: "/tmp/sock"}
	conn, err := net.DialUnix("unix", nil, &laddr)
	if err != nil {
		fmt.Println("Failed to connect:", err)
		return
	}
	defer conn.Close()
	r := bufio.NewReader(conn)
	w := bufio.NewWriter(conn)
	req := new(Request)
	req.Name = proto.String("apple")
	SendRequest(w, req)
	w.Flush()
	res, err := ReceiveResponse(r)
	if err != nil {
		fmt.Println("Failed to receive a response:", err)
		return
	}
	fmt.Println("res.Name =", *res.Name)
}
