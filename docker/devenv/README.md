# Start the dev environment

```shell
docker-compose up --build -d
```

- This command starts a container whith `devenv` name.
- This container runs OpenSSH server on port `8156`.
  You can connect to the sshd with `ssh -p 8156 $USER@localhost`.
- If you want to execute commands as `root` in the container, use `docker exec`.
- For example, `docker exec -it devenv bash`.
