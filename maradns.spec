Summary:	A (currently) authoritative-only DNS server made with security in mind
Name:		maradns
Version:	0.5.21
Release:	1
Copyright:	Public domain
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://www.maradns.org/download/%{name}-%{version}.tar.bz2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Erre con erre cigarro Erre con erre barril Rápido ruedan los carros En
el ferrocarril

MaraDNS is (currently) an authoritative-only DNS server made with
security in mind.

%prep
%setup -q 

%build
chmod +x configure
%configure
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man8,%{_sysconfdir},%{_sysconfdir}/maradns}
install server/maradns tuzona/zoneserver tuzona/getzone $RPM_BUILD_ROOT%{_sbindir}
install tools/askmara $RPM_BUILD_ROOT%{_bindir}
install doc/example_mararc $RPM_BUILD_ROOT%{_sysconfdir}/mararc
install doc/example_csv1 $RPM_BUILD_ROOT%{_sysconfdir}/maradns/db.example.com
install doc/man/maradns.8 $RPM_BUILD_ROOT%{_mandir}/man8/
gzip -9nf 00QuickStart CHANGELOG ROADMAP
find doc -type f -print |xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz doc/

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man8/maradns.8.gz
%config %{_sysconfdir}/mararc
%config %{_sysconfdir}/maradns/db.example.com
