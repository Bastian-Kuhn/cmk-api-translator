# CMK Translation API

## General


### /api/cmk
This API Deals with the wired Checkmk Version 1.x API Endpoints to
provide Simple Rest Endpoints to use with Service Now

Just surf to /api to see all available Endpoints

<img width="834" alt="Bildschirmfoto 2019-10-16 um 22 07 26" src="https://user-images.githubusercontent.com/899110/66955106-ff771900-f061-11e9-8c59-8559bfc4c85c.png">

### /api/graylog
Forwards Graylog Alerts to a in application/config.py configured Checkmk Eventkonsole Instance.
Make sure that the users this application is running, is member of a group who can access the socket.
It's also required to configure a login token which will be checked with each request.

<img width="834" alt="Bildschirmfoto 2020-09-11 um 19 41 36" src="https://user-images.githubusercontent.com/899110/92956349-01f71400-f467-11ea-8009-c3f5d6db7401.png">

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


 ## Deploy without Docker
 In /configs you will find a uwsgi file
