from fabric.api import local
from fabric.api import lcd

def prepare():
    local('pip freeze >| src/requirements.txt')
    local('git checkout master')
    local('git pull')
    local('git merge origin/develop')
    local('git push origin master')

def deploy():
    local('git pull')
    local('pip install --upgrade -r src/requirements.txt')
    local('python src/manage.py migrate')
    local('python src/manage.py test lukexor_me')
    local('python src/manage.py collectstatic --noinput --clear --link')
    local('echo -e "select 3\nflushdb" | redis-cli')
    local('echo -e "select 4\nflushdb" | redis-cli')
    local('sudo service apache2 graceful')
    local('python src/manage.py ping_google "/sitemap.xml"')
