image: simpleserver_deploy
	docker-compose build

simpleserver: simpleserver.go
	go build -o simpleserver simpleserver.go

# This rule build a statically-linked pure Go linux x86_64 binary.
simpleserver_deploy: simpleserver.go
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -o simpleserver_deploy simpleserver.go

clean:
	rm -f simpleserver simpleserver_deploy
