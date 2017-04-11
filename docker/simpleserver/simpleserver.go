package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

var (
	port = flag.Int("port", 8989, "Port number to listen.")
)

func fetchMessage() (_ string, err error) {
	res, err := http.Get("https://yunabe-codelab.appspot.com/hello?name=Go+In+Docker")
	if err != nil {
		return "", err
	}
	defer func() {
		cerr := res.Body.Close()
		if cerr == nil {
			return
		}
		if err == nil {
			err = cerr
		} else {
			err = fmt.Errorf("Failed to close: %v, internal error: %v", cerr, err)
		}
	}()
	b, err := ioutil.ReadAll(res.Body)
	if err != nil {
		return "", err
	}
	err = res.Body.Close()
	if err != nil {
		return "", err
	}
	return string(b), nil
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	msg, err := fetchMessage()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Add("Content-Type", "text/plain")
	_, err = w.Write([]byte(msg))
	if err != nil {
		log.Printf("Failed to write a response: %v", err)
	}
}

func main() {
	flag.Parse()
	http.HandleFunc("/", handleRequest)
	log.Printf("Listening on port %d", *port)
	err := http.ListenAndServe(fmt.Sprintf(":%d", *port), nil)
	if err != nil {
		log.Fatalf("Failed to start a HTTP server: %v", err)
	}
	log.Printf("A HTTP server is terminated.")
}
