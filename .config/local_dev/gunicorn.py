daemon = False
chdir = '/srv/smart-store-project/app'
bind = 'unix:/run/smartstore.sock'
accesslog = '/var/log/gunicorn/smartstore-access.log'
errorlog = '/var/log/gunicorn/smartstore-error.log'
capture_output = True