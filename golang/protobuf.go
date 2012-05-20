package main

import (
	"bytes"
	"fmt"
  "code.google.com/p/goprotobuf/proto"
	)	

func PrintToString(pb interface{}) string {
  buf := new(bytes.Buffer)
  proto.MarshalText(buf, pb)
  return buf.String()
}

func main() {
	p := Person {
	Name: proto.String("Taro Yamada"),
	Age: proto.Int32(8),
	};

	pet := Pet {Name: proto.String("Mike")}
	p.Pet = append(p.Pet, &pet)
	fmt.Println("-- p.String()  --")
	fmt.Println(p.String())
	fmt.Println("-- MarshalText --")
	fmt.Print(PrintToString(&p))  // not compact

	fmt.Println("-- Marshal --")
	m, _ := proto.Marshal(&p)
	fmt.Println(m)

	fmt.Println("-- CompactTextString --")
	fmt.Println(proto.CompactTextString(&p))
}
