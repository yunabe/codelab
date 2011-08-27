package main

import (
	"bytes"
	"fmt"
	"./example_pb"
	"goprotobuf.googlecode.com/hg/proto"
	)	

func PrintToString(pb interface{}) string {
  buf := new(bytes.Buffer)
  proto.MarshalText(buf, pb)
  return buf.String()
}

func main() {
	p := example.Person {
	Name: proto.String("Taro Yamada"),
	Age: proto.Int32(8),
	};

	pet := example.Pet {Name: proto.String("Mike")}
	p.Pet = append(p.Pet, &pet)
	fmt.Println("-- p.String()  --")
	fmt.Println(p.String())
	fmt.Println("-- MarshalText --")
	fmt.Print(PrintToString(&p))  // not compact
}
