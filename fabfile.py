from fabric.api import local
from fabric.api import lcd

def prepare():
    local('pip freeze >| src/requirements.txt')

def deploy():
    local('git pull')
    local('pip install --upgrade -r src/requirements.txt')
    local('python src/manage.py migrate')
    local('python src/manage.py test')
    local('python src/manage.py collectstatic --noinput --clear --link')
    local('sudo service apache2 graceful')
    local('python src/manage.py ping_google [/sitemap.xml]')
