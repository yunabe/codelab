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
- For example, 

# Login to the container via sshd as a non-root user
This container runs OpenSSH server on port `8156`.
To login to the container, execute

```shell
ssh -p 8156 $USER@localhost
```

When you rebuild the container image, the server-side key might change.
If you see `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` after you rebuild the container image,
run the following command to remove the old server key from `.ssh/known_hosts`.

```shell
ssh-keygen -R [localhost]:8156
```

# Execute commands as root.
- Interactive shell: `docker exec -it devenv bash`.
- Other commands: `docker exec devenv whoami`.

## Miscs
- [`docker build` and `docker-compose build` do not share the cache after `COPY` command.](https://github.com/docker/compose/issues/3148)
- [*All published (`-p` or `-P`) ports are exposed, but not all exposed (`EXPOSE` or `--expose`) ports are published.*](https://www.ctl.io/developers/blog/post/docker-networking-rules/)
