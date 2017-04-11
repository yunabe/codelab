# A sample pure-Go server and docker config to deploy it
- This sample builds a simple pure-Go server and a docker image to deploy it.
- Because this leverages the cross-compile feature,
- `CGO_ENABLED=0` is the easiest way to generate a statically-linked binary in Go
  if you do not use `cgo`.
- `CGO_ENABLED=0` is necessary if you use `net` package in linux.
- The root image of the docker image is Alpine Linux, not scratch
  because we want to install `ca-certificates` to the docker image.
  Without ca-certificates, your golang program can not connect to external servers over HTTPS.
- Please note that you may need to install additional things to your docker image
  if your program uses other Go packages.
  A statically linked binary does not necessarily means it does not have any dependencies to other files.
- Although the deployment of Go binary is relatively easy compared to other languages such as Java and Python,
  the deployment of a binary is still a tricky task because it's not trivial to fully understand what your program
  actually depends on.
