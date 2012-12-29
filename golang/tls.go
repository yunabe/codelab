package main

import (
	"bufio"
	"bytes"
	"crypto/tls"
	"crypto/x509"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

var serverCert *string = flag.String(
	"server_cert", "", "The path to a server certificate.")

var serverKey *string = flag.String(
	"server_key", "", "The path to a server private key.")

var clientAuthCert *string = flag.String(
	"client_auth_cert", "", "The path to a root certificate for client authentication")

func ServerFunc(w http.ResponseWriter, req *http.Request) {
	fmt.Println("ServerFunc:", req.URL.String())
	w.WriteHeader(200)
	io.WriteString(w, "Hello TLS\n")
}

func ListenAndServeTLS(addr string, certFile string, keyFile string, handler http.Handler) error {
	certPool := x509.NewCertPool()
	{
		fi, err := os.Open(*clientAuthCert)
		if err != nil {
			panic(err)
		}
		defer fi.Close()
		buf := new(bytes.Buffer)
		reader := bufio.NewReader(fi)
		io.Copy(buf, reader)
		if ok := certPool.AppendCertsFromPEM(buf.Bytes()); !ok {
			panic("Failed to append PEM.")
		}
	}
	server := &http.Server{
		Addr:    addr,
		Handler: handler,
		TLSConfig: &tls.Config{
			ClientAuth: tls.RequireAndVerifyClientCert,
			ClientCAs:  certPool,
		},
	}
	return server.ListenAndServeTLS(certFile, keyFile)
}

func main() {
	flag.Parse()
	ok := true
	if len(*serverCert) == 0 {
		log.Println("server_cert should not be empty.")
		ok = false
	}
	if len(*serverKey) == 0 {
		log.Println("server_key should not be empty.")
		ok = false
	}
	if len(*clientAuthCert) == 0 {
		log.Println("client_cert should not be empty.")
		ok = false
	}
	if !ok {
		return
	}

	http.HandleFunc("/", ServerFunc)
	err := ListenAndServeTLS(
		":8080",
		*serverCert,
		*serverKey,
		nil)
	if err != nil {
		log.Fatal("ListenAndServer: ", err)
	}
}
