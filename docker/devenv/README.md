# Pre-setup SSH keys

## SSH keys of the container
Create a new SSH key for the container.

```shell
ssh-keygen -f _ssh/id_rsa
```

## Copy a public key of your machine
Also, copy the public key of your machine to register it to the container.
Note that DSA keys are disabled by default in sshd from OpenSSH 7.

```shell
cat ~/.ssh/id_rsa.pub > _ssh/authorized_keys
```

# Run the dev environment

```shell
docker-compose up --build -d
```

- This command starts a container whith `devenv` name.
- This container runs OpenSSH server on port `8156`.
  You can connect to the sshd with `ssh -p 8156 $USER@localhost`.
- If you want to execute commands as `root` in the container, use `docker exec`.
- For example, `docker exec -it devenv bash`.
