# devenv
A directory to build a ubuntu-based Linux development environment using Vagrant and Ansible.

# Prerequisite
- Install Vagrant on your machine (e.g. Windows, Mac).
- Install Ansible on your machine.
- Create an ssh key pair for the dev environment.
  - `ssh-keygen -f ~/.ssh/devenv_id_rsa -C "devenv key"`

# Usage
- Build and start devenv VM
  - `cd` to this directory.
  - `vagrant up`
  - It takes about 1 hour for the initial provision.
- Suspend the VM
  - `vagrant suspend`
- Terminate the VM
  - `vagrant halt`
- Discard the VM
  - `vagrant destroy`
- Run ansible
  - `vagrant provision`
- Run ansible directory
  - `ansible-playbook playbook.yaml -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --private-key=.vagrant/machines/default/virtualbox/private_key`
- SSH to the VM
  - `vagrant ssh` or `ssh -p 2222 ubuntu@localhost -i .vagrant/machines/default/virtualbox/private_key`
- Create a box
  - Optional: Execute `sudo dd if=/dev/zero of=/EMPTY bs=1M; sudo rm -f /EMPTY` in the guest VM.
  - For example, the box file was compressed from 1.70GB to 1.44GB (16% reduction) by this.
  - `vagrant package --vagrantfile VagrantfileForBox --output devenv.box`
  - Use [devenv_prebuild](https://github.com/yunabe/codelab/tree/master/ansible/devenv) to run the box file.
  - Do not share the box file publicly. The box image contains some private keys which should not be share publickly.

# Misc
- List vagrant boxes: `vagrant box list`
- Update vagrant box: `vagrant box update --box ubuntu/xenial64`
- Delete old boxes after the update: `vagrant box prune`
- Run jupyter notebook accessible from the host: `jupyter notebook --port=8080 --ip=0.0.0.0`
