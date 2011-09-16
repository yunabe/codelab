package main

import (
	"encoding/binary"
	"fmt"
	"io"
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

func ReceiveResponse(reader io.Reader) (*Response, os.Error) {
	res := new(Response)
	if err := ReceiveProtoBuf(reader, res); err != nil {
		return nil, err
	}
	return res, nil
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

func SendRequest(writer io.Writer, req *Request) os.Error {
	return SendProtobuf(writer, req)
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
