# Mathieu Jadin, manifest to create Ubuntu VM with ipminet and routing daemons
$quagga_version = "1.2.1"
$quagga_release_url = "http://download.savannah.gnu.org/releases/quagga/quagga-${quagga_version}.tar.gz"
$quagga_root_dir = "/home/ubuntu"
$quagga_source_path = "${quagga_root_dir}/quagga-${quagga_version}"
$quagga_download_path = "${quagga_source_path}.tar.gz"
$quagga_path = "/home/ubuntu/quagga"

# Remove useless warnings
Package { allow_virtual => true }

# PATH
$default_path = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Exec { path => $default_path }

exec { 'apt-update':
  command => 'apt-get update',
}


# Python packages
package { 'python-setuptools':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'python-pip':
  require => [ Exec['apt-update'], Package['python-setuptools'] ],
  ensure => installed,
}
package { 'py2-ipaddress':
  require => Package['python-pip'],
  ensure => installed,
  provider => 'pip',
}
package { 'mako':
  require => Package['python-pip'],
  ensure => installed,
  provider => 'pip',
}
package { 'six':
  require => Package['python-pip'],
  ensure => installed,
  provider => 'pip',
}

# Networking
package { 'wireshark':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'radvd':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'traceroute':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'tcpdump':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'bridge-utils':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'mininet':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'ipmininet':
  provider => "pip", 
  require => [Package['mininet'],Package['mako'], Package['py2-ipaddress']],
  ensure => installed,
}

# Compilation
package { 'libreadline6':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'libreadline6-dev':
  require => [ Exec['apt-update'], Package['libreadline6'] ],
  ensure => installed,
}
package { 'gawk':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'automake':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'libtool':
  require => [ Exec['apt-update'], Package['m4'], Package['automake'] ],
  ensure => installed,
}
package { 'm4':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'bison':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'flex':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'pkg-config':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'dia':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'texinfo':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'libc-ares-dev':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'cmake':
  require => Exec['apt-update'],
  ensure => installed,
}

# Miscellaneous
package { 'xterm':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'man':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'git':
  require => Exec['apt-update'],
  ensure => installed,
}
package { 'valgrind':
  require => Exec['apt-update'],
  ensure => installed,
}

# Locale settings
exec { 'locales':
  require => Exec['apt-update'],
  command => "locale-gen fr_BE.UTF-8; update-locale",
}

# Main softwares

$compilation = [Exec['locales'], Package['libreadline6-dev'], Package['gawk'], Package['libtool'], Package['libc-ares-dev'],
                Package['bison'], Package['flex'], Package['pkg-config'], Package['dia'], Package['texinfo']]


exec { 'quagga-download':
  require => [ Exec['apt-update'] ],
  creates => $quagga_source_path,
  command => "wget -O - ${quagga_release_url} > ${quagga_download_path} &&\
              tar -xvzf ${quagga_download_path} -C ${quagga_root_dir};"
}

exec { 'quagga':
  require => [ Exec['apt-update'], Exec['quagga-download'] ] + $compilation,
  cwd => $quagga_source_path,
  creates => $quagga_path,
  path => "${default_path}:${quagga_source_path}",
  command => "configure --prefix=${quagga_path} &&\
              make &&\
              make install &&\
              rm ${quagga_download_path} &&\
              echo \"# quagga binaries\" >> /etc/profile &&\
              echo \"PATH=\\\"${quagga_path}/bin:${quagga_path}/sbin:\\\$PATH\\\"\" >> /etc/profile &&\
              echo \"alias sudo=\'sudo env \\\"PATH=\\\$PATH\\\"\'\" >> /etc/profile &&\
              echo \"# quagga binaries\" >> /root/.bashrc &&\
              echo \"PATH=\\\"${quagga_path}/bin:${quagga_path}/sbin:\\\$PATH\\\"\" >> /root/.bashrc &&\
              PATH=${quagga_path}/sbin:${quagga_path}/bin:\$PATH;",
}

# Quagga group

group { 'quagga':
	ensure => 'present',
}
user { 'ubuntu':
	groups => 'quagga',
}
user { 'root':
	groups => 'quagga',
}

