Summary:	A (currently) authoritative-only DNS server made with security in mind
Summary(pl):	Tylko autorytatywny (na razie) serwer DNS zrobiony z my¶l± o bezpieczeñstwie
Name:		maradns
Version:	0.8.35
Release:	2
License:	Public Domain
Group:		Networking/Daemons
Source0:	http://www.maradns.org/download/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Source2:	zoneserver.init
Source3:	mararc
Prereq:		/sbin/chkconfig
Prereq:		fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	bind
Conflicts:	djbdns

%description
MaraDNS is (currently) an authoritative-only DNS server made with
security in mind.

%description -l pl
MaraDNS jest (na razie) tylko autorytatywnym serwerem DNS zrobionym z
my¶l± o bezpieczeñstwie.

%package zoneserver
Summary:	Handle zone transfers for MaraDNS
Summary(pl):	Obs³uga transferów stref dla MaraDNS
Group:		Networking/Daemons
Requires:	maradns = %{version}
Prereq:		/sbin/chkconfig
Prereq:		fileutils

%description zoneserver
zoneserver listens on port 53/tcp and handles dns zone transfers.
zoneserver uses a configuration file, /etc/mararc by default, to
determine various parameters, such as the IP to bind to, who is
allowed to perform zone transfers, etc.

%description zoneserver -l pl
zoneserver s³ucha na porcie 53/tcp i obs³uguje transfery stref DNS.
U¿ywa domy¶lnie pliku konfiguracyjnego /etc/mararc aby uzyskaæ
parametry takie jak na jakim adresie ma s³uchaæ, kto mo¿e robiæ
transfery stref itp.

%prep
%setup -q

%build
%{__make} \
	CC=%{__cc} \
	FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/maradns,/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT%{_localstatedir}/log

install server/maradns tuzona/zoneserver tuzona/getzone $RPM_BUILD_ROOT%{_sbindir}
install tools/askmara $RPM_BUILD_ROOT%{_bindir}
install tools/benchmark $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/maradns
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/zoneserver
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/mararc
install doc/example_csv1 $RPM_BUILD_ROOT%{_sysconfdir}/maradns/db.example.com

> $RPM_BUILD_ROOT%{_localstatedir}/log/maradns
> $RPM_BUILD_ROOT%{_localstatedir}/log/zoneserver

install doc/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install doc/man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install doc/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

rm -rf doc/{man,detailed/man_macros}

gzip -9nf 0QuickStart TODO.* 00README.FIRST CREDITS \
	`find doc -type f -a -not -name \*.html`

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if ! id -g maradns > /dev/null 2>&1 ; then
        %{_sbindir}/groupadd -g 58 maradns
fi
if ! id -u maradns > /dev/null 2>&1 ; then
        %{_sbindir}/useradd -u 58 -g 58 -d /dev/null -s /bin/false -c "maraDNS user" maradns
fi

%post
/sbin/chkconfig --add maradns
if [ -f /var/lock/subsys/maradns ]; then
        /etc/rc.d/init.d/maradns restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/maradns start\" to start maradns" 1>&2
fi
touch %{_localstatedir}/log/maradns
chmod 640 %{_localstatedir}/log/maradns

%post zoneserver
/sbin/chkconfig --add zoneserver
if [ -f /var/lock/subsys/zoneserver ]; then
        /etc/rc.d/init.d/zoneserver restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/zoneserver start\" to start zoneserver" 1>&2
fi
touch %{_localstatedir}/log/zoneserver
chmod 640 %{_localstatedir}/log/zoneserver

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/maradns ]; then
                /etc/rc.d/init.d/maradns stop 1>&2
        fi
        /sbin/chkconfig --del maradns
fi

%preun zoneserver
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/zoneserver ]; then
                /etc/rc.d/init.d/zoneserver stop 1>&2
        fi
        /sbin/chkconfig --del zoneserver
fi

%postun
if [ "$1" = "0" ]; then
        %{_sbindir}/userdel maradns
        %{_sbindir}/groupdel maradns
fi

%files
%defattr(644,root,root,755)
%doc *.gz doc changelog.html

%attr(754,root,root) /etc/rc.d/init.d/maradns
%attr(755,root,root) %{_sbindir}/getzone
%attr(755,root,root) %{_sbindir}/maradns
%attr(755,root,root) %{_bindir}/*
%attr(0640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mararc
%attr(0640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/maradns/db.example.com
%attr(0640,root,root) %ghost %{_localstatedir}/log/maradns
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/maradns*

%files zoneserver
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/zoneserver
%attr(755,root,root) %{_sbindir}/zoneserver
%attr(640,root,root) %ghost %{_localstatedir}/log/zoneserver
%{_mandir}/man8/zoneserver*
