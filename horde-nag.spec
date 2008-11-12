%define		hordeapp nag
#
%include	/usr/lib/rpm/macros.php
Summary:	Nag Task List Manager
Summary(pl.UTF-8):	Nag - zarządca list zadań
Name:		horde-%{hordeapp}
Version:	2.3.1
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/nag/%{hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	4f2480c5fdb34fb34ee3cf7d1b320808
Source1:	%{hordeapp}.conf
Patch0:		%{hordeapp}-prefs.patch
URL:		http://www.horde.org/nag/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	horde >= 3.0
Requires:	webapps
Obsoletes:	%{hordeapp}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(/usr/share/horde.*)' 'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Nag is the Horde task list application. It stores todo items, things
due later this week, etc. It is very similar in functionality to the
Palm ToDo application.

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with Nag) please visit <http://www.horde.org/>.

%description -l pl.UTF-8
Nag to aplikacja do zarządzania zadaniami dla Horde. Przechowuje
rzeczy do zrobienia, płatności w danym tygodniu itp. Jest bardzo
podobna w funkcjonalności do aplikacji Palm ToDo.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Więcej informacji (włącznie z pomocą dla Naga)
można znaleźć na stronie <http://www.horde.org/>.

%prep
%setup -q -n %{hordeapp}-h3-%{version}

for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a js lib locale tasklists templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
If you are installing for the first time, You may need to
create the Nag database tables. To do so run:
zcat %{_docdir}/%{name}-%{version}/scripts/sql/%{hordeapp}.sql.gz | mysql horde
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/js
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/tasklists
%{_appdir}/templates
%{_appdir}/themes
