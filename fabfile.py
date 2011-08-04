from fabric.api import sudo, prompt, run, local, cd
from fabric.decorators import runs_once, hosts, task
from fabric.colors import green

@task
def ci():
    """Commit localy using mercurial"""
    comment = prompt('Commit comment: ', default='another commit from fabric')
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
@hosts('rif@84.1.105.44')
def deploy():
    'Deploy the app to the target environment'
    print(green('deploying...'))
    push()
    with cd('/Users/rif/bucatar'):
        run('hg up')

@task
@hosts('rif@84.1.105.44')
def reload():
    print(green('reloading...'))
    'fires an apache graceful reload'
    sudo('apachectl graceful')
