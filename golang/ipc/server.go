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

func ReceiveRequest(reader io.Reader) (*Request, os.Error) {
	req := new(Request)
	if err := ReceiveProtoBuf(reader, req); err != nil {
		return nil, err
	}
	return req, nil
}

func ReceiveProtoBuf(reader io.Reader, pb interface{}) os.Error {
	fmt.Println("ReceiveRequest...")
	var size uint64;
	if err := binary.Read(reader, binary.LittleEndian, &size); err != nil {
		return err
	}		
	fmt.Println("size =", size)
	buf := make([]byte, size)
	if _, err := io.ReadFull(reader, buf); err != nil {
		return err
	}
	return proto.Unmarshal(buf, pb)
}

func SendResponse(writer io.Writer, res *Response) os.Error {
	return SendProtobuf(writer, res)
}

func SendProtobuf(writer io.Writer, pb interface{}) os.Error {
	var data []byte
	var err os.Error
	if data, err = proto.Marshal(pb); err != nil {
		return err
	}
	size := uint64(len(data))
	binary.Write(writer, binary.LittleEndian, size)
	_, err = writer.Write(data)
	return err
}

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
