Summary:	A (currently) authoritative-only DNS server made with security in mind
Summary(pl.UTF-8):   Tylko autorytatywny (na razie) serwer DNS zrobiony z myślą o bezpieczeństwie
Name:		maradns
Version:	1.1.43
Release:	3
License:	Public Domain
Group:		Networking/Daemons
Source0:	http://www.maradns.org/download/1.1/%{name}-%{version}.tar.bz2
# Source0-md5:	cac028c40b3c2b5519c80481616397fb
Source1:	%{name}.init
Source2:	zoneserver.init
Source3:	mararc
Patch0:		%{name}-default_uid.patch
URL:		http://www.maradns.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/groupmod
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires:	rc-scripts
Provides:	group(named)
Provides:	nameserver
Provides:	user(named)
Obsoletes:	nameserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MaraDNS is (currently) an authoritative-only DNS server made with
security in mind.

%description -l pl.UTF-8
MaraDNS jest (na razie) tylko autorytatywnym serwerem DNS zrobionym z
myślą o bezpieczeństwie.

%package zoneserver
Summary:	Handle zone transfers for MaraDNS
Summary(pl.UTF-8):   Obsługa transferów stref dla MaraDNS
Group:		Networking/Daemons
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description zoneserver
zoneserver listens on port 53/tcp and handles dns zone transfers.
zoneserver uses a configuration file, /etc/mararc by default, to
determine various parameters, such as the IP to bind to, who is
allowed to perform zone transfers, etc.

%description zoneserver -l pl.UTF-8
zoneserver słucha na porcie 53/tcp i obsługuje transfery stref DNS.
Używa domyślnie pliku konfiguracyjnego /etc/mararc aby uzyskać
parametry takie jak na jakim adresie ma słuchać, kto może robić
transfery stref itp.

%prep
%setup -q
%patch0 -p1

# kill precompiled x86 objects
rm -f {parse,qual,tcp}/*.o

%build
%{__make} \
	CC="%{__cc}" \
	FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/{,fr/}man{1,5,8}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/maradns,/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT%{_localstatedir}/log

install server/maradns tcp/zoneserver tcp/getzone $RPM_BUILD_ROOT%{_sbindir}
install tools/askmara $RPM_BUILD_ROOT%{_bindir}
install tools/benchmark $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/maradns
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/zoneserver
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/mararc
install doc/en/examples/example_csv1 $RPM_BUILD_ROOT%{_sysconfdir}/maradns/db.example.com

> $RPM_BUILD_ROOT%{_localstatedir}/log/maradns
> $RPM_BUILD_ROOT%{_localstatedir}/log/zoneserver

install doc/en/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install doc/en/man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install doc/en/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install doc/fr/man/*.1 $RPM_BUILD_ROOT%{_mandir}/fr/man1
install doc/fr/man/*.5 $RPM_BUILD_ROOT%{_mandir}/fr/man5
install doc/fr/man/*.8 $RPM_BUILD_ROOT%{_mandir}/fr/man8

rm -rf doc/*/man

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 58 named
if [ "`/bin/id -u maradns 2>/dev/null`" = "58" ]; then
	/usr/sbin/usermod -d /tmp -l named maradns
fi
%useradd -u 58 -g 58 -d /tmp -s /bin/false -c "maraDNS user" named

%post
/sbin/chkconfig --add maradns
%service maradns restart
touch %{_localstatedir}/log/maradns
chmod 640 %{_localstatedir}/log/maradns

%postun
if [ "$1" = "0" ]; then
	%userremove named
	%groupremove named
fi

%post zoneserver
/sbin/chkconfig --add zoneserver
%service zoneserver restart
touch %{_localstatedir}/log/zoneserver
chmod 640 %{_localstatedir}/log/zoneserver

%preun
if [ "$1" = "0" ]; then
	%service maradns stop
	/sbin/chkconfig --del maradns
fi

%preun zoneserver
if [ "$1" = "0" ]; then
	%service zoneserver stop
	/sbin/chkconfig --del zoneserver
fi

%files
%defattr(644,root,root,755)
%doc 0QuickStart TODO 00README.FIRST CREDITS CHANGELOG doc/{README,en}
%lang(fr) %doc doc/fr
%attr(754,root,root) /etc/rc.d/init.d/maradns
%attr(755,root,root) %{_sbindir}/getzone
%attr(755,root,root) %{_sbindir}/maradns
%attr(755,root,root) %{_bindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mararc
%dir %{_sysconfdir}/maradns
%attr(640,root,root) %config %verify(not md5 mtime size) %{_sysconfdir}/maradns/db.example.com
%attr(640,root,root) %ghost %{_localstatedir}/log/maradns
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/maradns*
%{_mandir}/man8/duende*
%lang(fr) %{_mandir}/fr/man1/*
%lang(fr) %{_mandir}/fr/man5/*
%lang(fr) %{_mandir}/fr/man8/maradns*

%files zoneserver
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/zoneserver
%attr(755,root,root) %{_sbindir}/zoneserver
%attr(640,root,root) %ghost %{_localstatedir}/log/zoneserver
%{_mandir}/man8/zoneserver*
%lang(fr) %{_mandir}/fr/man8/zoneserver*
