import os
import re
import sys
from fabric.api import local
from fabric.api import lcd

sys.path.append('/home/caeledh/www/lukeworks.tech/public_html/src/')
sys.path.append('/home/caeledh/www/lukeworks.tech/public_html/src/lukexor_me')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lukexor_me.settings")

def read_env():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the project root
    directory.
    """
    try:
        with open('.env') as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)


def prepare():
    read_env()
    local('pip freeze >| src/requirements.txt')
    local('git checkout master')
    local('git pull')
    local('git merge origin/develop')
    local('git push origin master')

def update():
    read_env()
    local('git pull')
    local('pip install --upgrade -r src/requirements.txt')
    local('python src/manage.py migrate')

def test():
    read_env()
    local('python src/manage.py test lukexor_me')

def deploy():
    read_env()
    local('python src/manage.py collectstatic --noinput --clear --link')
    clear_cache()
    local('sudo systemctl restart nginx uwsgi')

def update_sitemap():
    local('python src/manage.py ping_google "/sitemap.xml"')

def clear_cache():
    local('echo "select 3\nflushdb" | redis-cli')
    local('echo "select 4\nflushdb" | redis-cli')
