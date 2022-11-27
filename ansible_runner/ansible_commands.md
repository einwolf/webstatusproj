# Running ansible-runner

## Ansible command examples

```bash
ansible-playbook -v -l redhat -e "ansible_user=localsysadmin" ping.yaml -k -b -K
ansible-playbook -v -l redhat -u localsysadmin ping.yaml -k -b -K
```

## ansible-runner command examples

The env/passwords prompt file is talking to ansible (not ssh).

```bash
ansible-runner run . -p ping.yaml
ansible-runner run --debug ~/github-einwolf/WebStatusProject1/ansible --limit redhat -p ping.yaml
```
