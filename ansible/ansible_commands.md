# Ansible command examples

```bash
ansible-playbook -v -l redhat -u localsysadmin ping.yaml -k -b -K
ansible-playbook -v -l redhat -e "ansible_user=localsysadmin" ping.yaml -k -b -K
```

## Environment variables

ANSIBLE_STDOUT_CALLBACK
