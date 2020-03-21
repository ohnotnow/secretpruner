#!/usr/bin/env python

import docker
import re
import dateutil.parser
import sys

client = docker.from_env()
date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}') # yyyy-mm-dd-hh-mm-ss
split_key = '-dotenv-'
keep = 5
secret_counts = {}
secret_list = {}
exit_code = 0

def prune_secrets(name):
    global exit_code
    pattern = re.compile(rf'^{name}')
    secrets = {}
    for secret_name, date_id in secret_list.items():
        if pattern.match(secret_name):
            secrets[secret_name] = date_id
    sorted_secrets = sorted(secrets.items(), key=lambda x: x[1][0])
    sorted_secrets.reverse()
    to_remove = []
    while len(sorted_secrets) > keep:
        to_remove.append(sorted_secrets.pop())
    for secret in to_remove:
        print(f"Removing secret {secret[0]} last updated at {secret[1][0]}")
        try:
            real_secret = client.secrets.get(secret[1][1])
            real_secret.remove()
        except:
            print(f"Error removing secret {secret[0]}")
            exit_code = 1

for secret in client.secrets.list():
    parts = secret.name.split(split_key)
    if date_pattern.match(parts[1]):
        if parts[0] not in secret_counts:
            secret_counts[parts[0]] = 0
        secret_counts[parts[0]] = secret_counts[parts[0]] + 1
        secret_list[secret.name] = [dateutil.parser.parse(secret.attrs['UpdatedAt']), secret.id]

for name, count in secret_counts.items():
    if count > keep:
        prune_secrets(name)

sys.exit(exit_code)
