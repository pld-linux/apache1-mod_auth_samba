%define		mod_name	auth_samba
Summary:	This is the samba authentication module for Apache
Summary(pl):	Modu³ autentykacji samba dla Apache
Name:		apache-mod_%{mod_name}
Version:	1.1
Release:	3
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://download.sourceforge.net/pub/sourceforge/modauthsamba/mod_%{mod_name}-%{version}.tar.gz
Patch0:		%{name}-symbol_fix.patch
URL:		http://modauthsamba.sourceforge.net/
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache(EAPI)-devel
BuildRequires:	gdbm-devel
BuildRequires:	pam-devel
BuildRequires:	pam_smb
Prereq:		/usr/sbin/apxs
Requires:	pam_smb
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using user entries in an samba directory.

%description -l pl
To jest modu³ autentykacji dla Apache pozwalaj±cy na autentykacjê
klientów HTTP z u¿yciem wpisów w katalogu samby.

%prep 
%setup -q -n mod_%{mod_name}
%patch0 -p1

%build
/usr/sbin/apxs -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lgdbm -lcrypt -lpam /lib/security/pam_smb_auth.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.html
%attr(755,root,root) %{_pkglibdir}/*
