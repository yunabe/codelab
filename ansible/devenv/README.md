# Prerequisite
- `ssh-keygen -f ~/.ssh/devenv_id_rsa -C "devenv key"`

# Usage
- Build and start devenv VM
  - `vagrant up`
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
  - `vagrant package --output devenv.box`

# Misc
- List vagrant boxes: `vagrant box list`
- Update vagrant box: `vagrant box update --box ubuntu/xenial64`
- Delete old boxes after the update: `vagrant box prune`
