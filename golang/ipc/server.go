package main

import (
	"bufio"
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"os"

	"goprotobuf.googlecode.com/hg/proto"
	)


func ReceiveRequest(reader io.Reader) *Request {
	fmt.Println("ReceiveRequest...")
	var size uint64;
	if err := binary.Read(reader, binary.LittleEndian, &size); err != nil {
		fmt.Println("Failed to read size:", err)
		return nil
	}		
	fmt.Println("size =", size)
	buf := make([]byte, size)
	if _, err := io.ReadFull(reader, buf); err != nil {
		fmt.Println("Failed to data.")
		return nil
	}
	req := new(Request)
	if err := proto.Unmarshal(buf, req); err != nil {
		fmt.Println("Failed to unmarshal")
		return nil
	}
	return req
}

func SendResponse(res *Response, writer io.Writer) {
	var data []byte
	var err os.Error
	if data, err = proto.Marshal(res); err != nil {
		fmt.Println("Failed to marshal...")
	}
	size := uint64(len(data))
	fmt.Println("size =", size)
	binary.Write(writer, binary.LittleEndian, size)
	n, err := writer.Write(data)
	fmt.Println(n, err)
}

func handleConnection(conn *net.UnixConn) {
	defer conn.Close()
	defer fmt.Println("closing...")
	r := bufio.NewReader(conn)
	w := bufio.NewWriter(conn)

	req := ReceiveRequest(r)
	if req != nil {
		fmt.Println("req.Name =", *req.Name)
		res := new(Response)
		res.Name = proto.String("hello hello!")
		SendResponse(res, w)
		w.Flush()
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
		go handleConnection(c)
	}
}
