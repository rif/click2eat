$home = '/home/rif'
$data_dir = '/home/www-data'
$ssl_dir = '/etc/nginx/ssl'
$venv_dir = '/home/rif/.virtualenvs'

package {
	'mercurial': ensure => installed;
    	'bzr': ensure => installed;
	'git': ensure => installed;
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
	'libhiredis-dev': ensure => installed;
    	'libjpeg8-dev': ensure => installed;
    	'libfreetype6-dev': ensure => installed;
	'update-notifier-common': ensure => installed;
	'python-twisted': ensure => installed;
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

file { '/etc/supervisor/conf.d/kippo.conf':
	ensure => link,
	target => '/home/www-data/bucatar/apache/supervizor/kippo.conf' 
}


file { '/etc/nginx/sites-available/bucatar':
	ensure => link,
	target => '/home/www-data/bucatar/apache/bucatar.nginx',
	require => Package['nginx']
}

file { '/etc/nginx/sites-enabled/bucatar':
	ensure => link,
	target => '/etc/nginx/sites-available/bucatar',
	require => Package['nginx']
}

file { '/etc/nginx/sites-available/maintenance':
	ensure => link,
	target => '/home/www-data/bucatar/apache/maintenance.nginx',
	require => Package['nginx']
}

file { '/etc/nginx/sites-enabled/default':
	ensure => absent,
	require => Package['nginx']
}

file { '/etc/uwsgi/apps-available/bucatar.xml':
	ensure => link,
	target => '/home/www-data/bucatar/apache/bucatar.xml',
	require => Package['uwsgi']
}

file { '/etc/uwsgi/apps-enabled/bucatar.xml':
	ensure => link,
	target => '/etc/uwsgi/apps-available/bucatar.xml',
	require => Package['uwsgi']
}

exec { 'hg clone ssh://hg@bitbucket.org/rif/click2eat':
	path => '/usr/bin/',
	cwd => $data_dir,
	require => File['/home/www-data'],
	creates => '/home/www-data/bucatar'
}

file { $ssl_dir:
	ensure => directory,
	require => Package['nginx']
}

exec { 'key':
    command => '/usr/bin/openssl genrsa -out bucatar.key 1024',
	cwd => $ssl_dir,
	require => File[$ssl_dir],
	creates => '/etc/nginx/ssl/bucatar.key'
}

exec { 'csr':
    command  => '/usr/bin/openssl req -batch -new -key bucatar.key -out bucatar.csr',
    cwd => $ssl_dir,
    require => Exec['key'],
    creates => '/etc/nginx/ssl/bucatar.csr'
}

exec { 'crt':
    command => '/usr/bin/openssl x509 -req -days 1780 -in bucatar.csr -signkey bucatar.key -out bucatar.crt',
    cwd => $ssl_dir,
    require => Exec['csr'],
    creates => '/etc/nginx/ssl/bucatar.crt'
}

#exec { '/usr/bin/mysql_secure_installation':
#	require => Package['mysql-server'],
#}

file { $venv_dir:
	ensure => directory,
	owner => 'rif',
	group => 'rif',
	require => Package['virtualenvwrapper']
}

exec {
	'virtualenv --no-site-packages bucatar': cwd => $venv_dir, path => '/usr/bin', require => File[$venv_dir], user => 'rif', creates => '/home/rif//.virtualenvs/bucatar';
#	'virtualenv --no-site-packages trac': cwd => $venv_dir, path => '/usr/bin', require => File[$venv_dir], user => 'rif', creates => '/home/rif//.virtualenvs/trac';
#	'virtualenv --no-site-packages sentry': cwd => $venv_dir, path => '/usr/bin', require => File[$venv_dir], user => 'rif', creates => '/home/rif//.virtualenvs/bucatar/sentry';
}
