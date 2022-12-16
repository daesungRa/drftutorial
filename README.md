# DRF 튜토리얼 공부용

Django REST Framework 학습을 위해
**[공식 홈페이지](https://www.django-rest-framework.org/)** 에서 튜토리얼을 진행합니다.

<br>

---

# How to run project?

In a Linux bash shell environment,

## Installation

- _Create project root_

```text
/pjt/root $ mkdir drftutorial
/pjt/root $ cd drftutorial
/pjt/root/drftutorial $ git init
/pjt/root/drftutorial $ git remote add upstream https://github.com/daesungRa/drftutorial.git
/pjt/root/drftutorial $ git pull upstream master
```

- _Update and Set virtual env_

```text
/pjt/root/drftutorial $ python --version
Python 3.x.x
/pjt/root/drftutorial $ pip --version
pip xx.x.x from /public/python/root/pip (python 3.x)
/pjt/root/drftutorial $ python -m pip install --upgrade pip
/pjt/root/drftutorial $ python -m pip install virtualenv
/pjt/root/drftutorial $ python -m pip install --upgrade virtualenv
```

## Configuration

Let's make a virtual environment and install the required packages using requirements.txt.

```text
/pjt/root/drftutorial $ python -m virtualenv venv
/pjt/root/drftutorial $ source ./venv/bin/activate
(venv) /pjt/root/drftutorial $ pip --version
pip xx.x.x from /pjt/root/drftutorial/venv/lib/site-packages/pip (python 3.x)
(venv) /pjt/root/drftutorial $ pip install -r requirements.txt
(venv) /pjt/root/drftutorial $ python manage.py migrate
```

## Start project!

```text
(venv) /pjt/root/drftutorial $ python manage.py runserver
...
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

```

and access **<a href="http://127.0.0.1:8000/" target="_blank">here</a>**

Done!
