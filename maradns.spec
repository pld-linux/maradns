Summary:	A (currently) authoritative-only DNS server made with security in mind
Name:		maradns
Version:	0.8.26
Release:	1
License:	Public domain
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://www.maradns.org/download/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Source2:	mararc
Conflicts:	bind
Conflicts:	djbdns
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Erre con erre cigarro Erre con erre barril Rápido ruedan los carros En
el ferrocarril

MaraDNS is (currently) an authoritative-only DNS server made with
security in mind.

%prep
%setup -q 

%build
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{maradns,rc.d/init.d}
install server/maradns tuzona/zoneserver tuzona/getzone $RPM_BUILD_ROOT%{_sbindir}
install tools/askmara $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/maradns
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/mararc
install doc/example_csv1 $RPM_BUILD_ROOT%{_sysconfdir}/maradns/db.example.com
mv doc/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
mv doc/man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5/
mv doc/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/
rm -rf doc/man
gzip -9nf 0QuickStart TODO.*  00README.FIRST CREDITS 

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

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/maradns ]; then
                /etc/rc.d/init.d/maradns stop 1>&2
        fi
        /sbin/chkconfig --del maradns
fi

%postun
if [ "$1" = "0" ]; then
        %{_sbindir}/userdel maradns
        %{_sbindir}/groupdel maradns
fi


%files
%defattr(644,root,root,755)
%doc *.gz doc/ changelog.html

%attr(754,root,root)  /etc/rc.d/init.d/maradns
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%config %{_sysconfdir}/mararc
%config %{_sysconfdir}/maradns/db.example.com
