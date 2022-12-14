import json
import logging
import os
import subprocess
from pathlib import Path

from ansparse.AnsibleParsePing import AnsibleParsePing

def main():
    playbook_path = "ping.yaml"

    result = run_ansible_playbook(playbook_path)

    with open("json_result.json", "w+") as json_file:
        json_file.write(json.dumps(result, indent=4, sort_keys=True))

    ap = AnsibleParsePing(result)
    ap.parse_json()

    print(ap.result)

    return 0


def run_ansible_playbook(playbook_path):
    env = os.environ.copy()
    env["ANSIBLE_STDOUT_CALLBACK"] = "json"
    
    # Get usernames and passwords
    with open("user_passwords.json", "r") as user_file:
        user_passwords = json.loads(user_file.read())

    up_args = [f'{k}={v}' for k,v in user_passwords.items()]
    
    args = [
        "ansible-playbook",
        "-v",
        "-l", "redhat",
        "-b",
    ]

    for var in up_args:
        args.append("-e")
        args.append(var)

    args.append(playbook_path)

    print(f"{args=}")
    print(f"{' '.join(args)}")
    result = subprocess.run(args, env=env, shell=False, stdin=None, capture_output=True, encoding="utf-8")

    # Check return result
    if result.returncode > 0:
        # There are many result codes that are ok
        # 4 - one or more unreachable hosts
        pass

    # Passing -v causes non-json text to be output before the json part (ansible 2.9)
    json_start = result.stdout.find("{")
    stdout = result.stdout[json_start:]

    json_result = json.loads(stdout)

    return json_result


if __name__ == "__main__":
    main()
