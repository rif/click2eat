from fabric.api import hosts, prompt, sudo, run, local, cd

def ci():
    """Commit localy using mercurial"""
    comment = prompt('Commit comment: ', default='another commit from fabric')
    local('hg ci -m "%s"' % comment)
    local('hg push')

"""
For running sudo on remote machine:
    vi /etc/sudoers (EDIT: please use visudo instead)
    comment out: #Default requiretty
"""
@hosts('rif@84.1.105.44')
def deploy():
    'Deploy the app to the target environment'
    local('hg push')
    with cd('/Users/rif/bucatar'):
        run('hg up')

@hosts('rif@84.1.105.44')
def reload():
    'fires an apache graceful reload'
    sudo('apachectl graceful')
