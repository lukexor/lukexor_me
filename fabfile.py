from fabric.api import local
from fabric.api import lcd

def deploy():
    local('git pull')
    local('pip install --upgrade -r src/requirements.txt')
    local('python src/manage.py migrate')
    local('python src/manage.py test')
    local('python src/manage.py collectstatic --noinput --clear --link')
    local('sudo service apache2 graceful')
