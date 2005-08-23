# TODO
# - rename nag.spec to tldp-nag.spec
# - rename this spec to nag.spec
# - or forget it and rename all horde packages to horde-*.spec

#define	_rc		rc1
%define	_rel	0.3

%define		_hordeapp	nag
%include	/usr/lib/rpm/macros.php
Summary:	Nag Task List Manager
Summary(pl):	Nag - zarz�dca list zada�
Name:		nag
Version:	2.0.2
Release:	%{?_rc:%{_rc}.}%{_rel}
License:	GPL v2
Vendor:		The Horde Project
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/nag/%{_hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	7aa928522dadda94f02dfcbc5fb90058
Source1:	%{name}.conf
Patch0:		%{name}-prefs.patch
URL:		http://www.horde.org/nag/
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir		/usr/share/horde
%define		_sysconfdir		/etc/horde.org
%define		_appdir			%{hordedir}/%{_hordeapp}

%description
Nag is the Horde task list application. It stores todo items, things
due later this week, etc. It is very similar in functionality to the
Palm ToDo application.

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with Nag) please visit <http://www.horde.org/>.

%description -l pl
Nag to aplikacja do zarz�dzania zadaniami dla Horde. Przechowuje
rzeczy do zrobienia, p�atno�ci w danym tygodniu itp. Jest bardzo
podobna w funkcjonalno�ci do aplikacji Palm ToDo.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Wi�cej informacji (w��cznie z pomoc� dla
Naga) mo�na znale�� na stronie <http://www.horde.org/>.

%prep
%setup -q -n %{?_snap:nag}%{!?_snap:nag-h3-%{version}%{?_rc:-%{_rc}}}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.daily,%{_sysconfdir}/%{_hordeapp}} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,scripts,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php
install  config/conf.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
> $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR	lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR	templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR	themes/*		$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
If you are installing for the first time, You may need to
create the Nag database tables. To do so run:
zcat %{_docdir}/%{name}-%{version}/scripts/sql/nag.sql.gz | mysql horde
EOF
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
