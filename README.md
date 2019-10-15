# CMK Translation API

## General

This API Deals with the wired Checkmk API Endpoints to
provide Simple Rest Endpoints to use with Service Now


## Local Testing without Docker
### SETUP
 - Create Virtual Environtment:
 - On Mac: _virtualenv --no-site-packages --distribute -p /usr/local/bin/python3.X ENV_ (Creates the Environment)
 - On Linux: _virtualenv --no-site-packages --distribute -p /usr/bin/python3.X ENV_ (Creates the Environment)
 - (or short _python3 -m venv ENV_ if you know what you do
 - Change inside with _source ENV/bin/activate_
 - Install requirements with _pip install -r requirements.txt_

## UnitTests
  - source ENV/bin/activate
  - ./manage test

### 
 - Enable virtual env (source ENV/bin/activate)
 -  _./manage.py runserver_


 ## Docker
 Just run Container. The Container Exposes port 9090. There is UWSGI behind.


 ## Deplpoy without Docker
 In /configs you will find a uwsgi file
