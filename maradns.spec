Summary:	A (currently) authoritative-only DNS server made with security in mind
Summary(pl):	Tylko autorytatywny (na razie) serwer DNS zrobiony z my¶l± o bezpieczeñstwie
Name:		maradns
Version:	1.1.22
Release:	1
License:	Public Domain
Group:		Networking/Daemons
Source0:	http://www.maradns.org/download/1.1/%{name}-%{version}.tar.bz2
# Source0-md5:	e7f2d1d61c551aaa31373d5b334f9307
Source1:	%{name}.init
Source2:	zoneserver.init
Source3:	mararc
PreReq:		rc-scripts
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	nameserver

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
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils
Requires:	%{name} = %{version}

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

rm -rf doc/{man,detailed/man_macros}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid maradns`" ]; then
	if [ "`getgid maradns`" != "58" ]; then
		echo "Error: group maradns doesn't have gid=58. Correct this before installing maradns." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 58 maradns
fi
if [ -n "`id -u maradns 2>/dev/null`" ]; then
	if [ "`id -u maradns`" != "58" ]; then
		echo "Error: user maradns doesn't have uid=58. Correct this before installing maradns." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 58 -g 58 -d /dev/null -s /bin/false -c "maraDNS user" maradns
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

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel maradns
	/usr/sbin/groupdel maradns
fi

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

%files
%defattr(644,root,root,755)
%doc 0QuickStart TODO 00README.FIRST CREDITS doc CHANGELOG
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
