#!/usr/bin/env python3


import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('cmd', type=str, nargs=argparse.REMAINDER, default='')
args = parser.parse_args()

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    ('-p', '8001:80'),
    ('--name', 'smartstore-test'),
]

DOCKER_NAME = 'smartstore-test'
DOCKER_IMAGE_TAG = 'johnkdo2020/smartstore-test'

subprocess.run(f'poetry export -f requirements.txt > requirements.txt', shell=True)
subprocess.run(f'sudo docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)
print('sudo docker build')
subprocess.run(f'sudo docker stop smartstore-test', shell=True)
# subprocess.run(f'sudo docker stop {DOCKER_NAME}', shell=True)
print('sudo docker stop')
subprocess.run('sudo docker run {options} {tag} /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)
#
subprocess.run(f'sudo docker cp secrets.json {DOCKER_NAME}:/srv/smart-store-project', shell=True)
print('sudo docker copy secret')
# collectstatic을 subprocess.run()을 사용해서 실행
subprocess.run(f'sudo docker exec {DOCKER_NAME} python manage.py collectstatic --noinput', shell=True)
print('sudo docker copy static file')
# 실행중인 name=instagram인 container에서 argparse로 입력받은 cmd또는 bash를 실행(foreground 모드)
subprocess.run('sudo docker exec -it smartstore-test {cmd}'.format(
    cmd=' '.join(args.cmd) if args.cmd else 'supervisord -c ../.config/local_dev/supervisord.conf -n'
), shell=True)
