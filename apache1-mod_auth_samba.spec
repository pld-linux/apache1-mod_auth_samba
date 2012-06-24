# TODO
# - Cannot load mod_auth_samba.so into server: mod_auth_samba.so: undefined symbol: dbm_fetch
%define		mod_name	auth_samba
%define 	apxs	/usr/sbin/apxs1
Summary:	This is the samba authentication module for Apache
Summary(pl):	Modu� uwierzytelnienia samba dla Apache
Name:		apache1-mod_%{mod_name}
Version:	1.1
Release:	3
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modauthsamba/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	9478a055e5cedd8c00beaed83d324240
Patch0:		%{name}-symbol_fix.patch
URL:		http://modauthsamba.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	gdbm-devel
BuildRequires:	pam-devel
BuildRequires:	pam-pam_smb
Requires(triggerpostun):	%{apxs}
Requires:	apache1 >= 1.3.33-2
Requires:	pam-pam_smb
Obsoletes:	apache-mod_%{mod_name} <= %{epoch}:%{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)
%define		_noautoreq	/%{_lib}/security/pam_smb_auth.so

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using user entries in an samba directory.

%description -l pl
To jest modu� uwierzytelnienia dla Apache pozwalaj�cy na
uwierzytelnianie klient�w HTTP z u�yciem wpis�w w katalogu samby.

%prep
%setup -q -n mod_%{mod_name}
%patch0 -p1

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so \
	-lgdbm -lcrypt -lpam /%{_lib}/security/pam_smb_auth.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1:1.1-2.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc *.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
