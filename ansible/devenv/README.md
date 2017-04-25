# Usage
- Build and start devenv VM: `vagrant up`
- Discard the VM: `vagrant destroy`
- Run ansible directory: `ansible-playbook playbook.yaml -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --private-key=.vagrant/machines/default/virtualbox/private_key`
- SSH to the VM: `vagrant ssh` or `ssh -p 2222 ubuntu@localhost -i .vagrant/machines/default/virtualbox/private_key`

# Misc
- List vagrant boxes: `vagrant box list`
- Update vagrant box: `vagrant box update --box ubuntu/xenial64`
- Delete old boxes after the update: `vagrant box prune`
