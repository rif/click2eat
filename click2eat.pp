$home = '/home/rif'
$data_dir = '/home/www-data'

package {
	'mercurial': ensure => installed;
    	'bzr': ensure => installed;
    	'subversion': ensure => installed;
	'zile': ensure => installed;
    	'nginx': ensure => installed;
    	'uwsgi': ensure => installed;
    	'uwsgi-plugin-python': ensure => installed;
    	'mysql-server': ensure => installed;
    	'mysql-client': ensure => installed;
    	'supervisor': ensure => installed;
    	'build-essential': ensure => installed;
    	'python-pip': ensure => installed;
    	'python-dev': ensure => installed;
    	'python-virtualenv': ensure => installed;
    	'virtualenvwrapper': ensure => installed;
    	'libmysqlclient-dev': ensure => installed;
    	'redis-server': ensure => installed;
    	'libjpeg8-dev': ensure => installed;
    	'libfreetype6-dev': ensure => installed;
	'update-notifier-common': ensure => installed;
}

file { '/home/www-data':
	ensure => directory,
	owner => 'rif',
	group => 'rif'
}

file { '/etc/supervisor/conf.d/celeryd.conf':
	ensure => link,
	target => '/home/www-data/bucatar/apache/supervizor/celeryd.conf' 
}

exec { 'hg clone ssh://hg@bitbucket.org/rif/click2eat':
	path => $data_dir,
	require => File['/home/www-data'],
	unless => 'ls /home/www-data/bucatar'
}

exec {
    'mkvirtualenv --no-site-packages bucatar': path => $home, require => Package['virtualenvwrapper']
#    'mkvirtualenv  trac': path => $home;
#    'mkvirtualenv --no-site-packages sentry': path => $home;
}