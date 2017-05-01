# Prebuild devenv
A directory to run the prebuild devenv VirtualBox VM with Vagrant.

# Usage
- [Build a box file for the development environment.](https://github.com/yunabe/codelab/tree/master/ansible/devenv)
- Import `devenv.box`
  - `vagrant box add devenv /path/to/devenv.box`
  - If your machine already has `devenv`, delete it with `vagrant box remove devenv`.
- Start the VM
  - `vagrant up`
