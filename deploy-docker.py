#!/usr/bin/env python3
import os
import subprocess
import json
from pathlib import Path

with open('./secrets.json') as json_file:
    SECRETS_FULL = json.load(json_file)
    SECRETS_BASE = SECRETS_FULL['base']

PROJECT_NAME = 'smart-store-project'
USER = 'ubuntu'
HOST = SECRETS_BASE['HOST']
TARGET = f'{USER}@{HOST}'
HOME = str(Path.home())
print(HOME)
DOCKER_NAME = 'smartstore'
DOCKER_IMAGE = f'johnkdo2020/{DOCKER_NAME}'
DOCKER_IMAGE_TAG = 'smartstore_tag'

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    # background로 실행하는 옵션 추가
    ('-d', ''),
    ('-p', '80:80'),
    ('-p', '5000:5000'),
    ('--name', DOCKER_NAME),
]

IDENTITY_FILE = os.path.join(HOME, '.ssh', 'smartstore.pem')
SOURCE = os.path.join(HOME, 'projects', 'personal_project', 'smartmarket')
SECRETS_FILE = os.path.join(SOURCE, 'smart-store-project', 'secrets.json')


# FRONT_DIR = os.path.join(SOURCE, 'smart-store-react', 'test-code')


def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()


def ssh_run(cmd, ignore_error=False):
    run(f"ssh -o StrictHostKeyChecking=no -i {IDENTITY_FILE} {TARGET} -C {cmd}", ignore_error=ignore_error)


def local_build_push():
    print('*********************build**********************')
    run(f'pip freeze > requirements.txt')
    run(f'sudo docker build -t {DOCKER_IMAGE} .')
    run(f'sudo docker push {DOCKER_IMAGE}')
    print('build finish*************************')


def server_init():
    print('*******************server init ************************')
    ssh_run(f'sudo apt update')
    ssh_run(f'sudo apt --fix-broken install -y')
    ssh_run(f'sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y')
    # ssh_run(f'sudo apt list --upgradable')
    ssh_run(f'sudo apt -y install docker.io')


def server_pull_run():
    print('*******************server docker hub pull ************************')
    ssh_run(f'sudo docker stop {DOCKER_NAME}', ignore_error=True)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE}')
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE,
    ))
    print('*******************server docker pull completed ************************')


def copy_secrets():
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} {TARGET}:/tmp', ignore_error=True)
    # run(f'sudo scp -i {IDENTITY_FILE} -r {FRONT_DIR} {TARGET}:/srv -y', ignore_error=True)
    print('**************************scp secrets*******************')
    ssh_run(f'sudo docker cp /tmp/secrets.json {DOCKER_NAME}:/srv/{PROJECT_NAME}')

    print('*******************copy secrets************************')


def server_cmd():
    ssh_run(f'sudo docker exec smartstore /usr/sbin/nginx -s stop', ignore_error=True)
    # ssh_run(f'sudo docker exec smartstore pip install "django<3.0"', ignore_error=True)
    print('**********************server nginx stop*********************')
    ssh_run(f'sudo docker exec smartstore python manage.py collectstatic --noinput', ignore_error=True)
    print('*******************collect static************************')
    ssh_run(f'sudo docker exec smartstore python manage.py makemigrations', ignore_error=True)
    print('**********************migrate***************************')
    ssh_run(f'sudo docker exec smartstore python manage.py migrate')
    # ssh_run(f'sudo docker exec -it -d smartstore '
    #         f'npx serve -s -c /srv/smart-store-project/front/build')
    ssh_run(f'sudo docker exec -it -d smartstore '
            f'supervisord -c /srv/smart-store-project/.config/local_dev/supervisord.conf -n')
    print('**********************manage***************************')


if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_secrets()
        server_cmd()
    except subprocess.CalledProcessError as e:
        print('deploy Error')
        print(' cmd:', e.cmd)
        print(' returncode:', e.returncode)
        print(' output:', e.output)
        print(' stdout:', e.stdout)
        print(' stderr:', e.stderr)
