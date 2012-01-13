from fabric.api import sudo, prompt, run, local, cd, parallel
from fabric.decorators import runs_once, task, hosts
from fabric.colors import green

@task
def ci():
    """Commit localy using mercurial"""
    comment = prompt('Commit comment: ', default='another commit from fabric')
    local('compass compile -e production --force media')
    local('hg ci -m "%s"' % comment)
    push()

@runs_once
def push():
    print(green('pushing...'))
    local('hg push')

"""
For running sudo on remote machine:
    vi /etc/sudoers (EDIT: please use visudo instead)
    comment out: #Default requiretty
"""
@task
@parallel
@hosts('rif@click2eat.ro:22011', 'rif@demo.click2eat.ro:22011')
def deploy():
    """Deploy the app to the target environment"""
    print(green('deploying...'))
    push()
    with cd('/home/www-data/bucatar'):
        run('hg pul -uv')
        run('source /etc/bash_completion.d/virtualenvwrapper; workon bucatar; python manage.py collectstatic --noinput')

@task
@hosts('rif@click2eat.ro:22011', 'rif@demo.click2eat.ro:22011')
def reload():
    print(green('reloading...'))
    'fires an uwsgi graceful reload'
    sudo('service uwsgi reload')
