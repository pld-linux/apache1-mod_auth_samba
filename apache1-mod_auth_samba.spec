%define		mod_name	auth_samba
%define 	apxs	/usr/sbin/apxs1
Summary:	This is the samba authentication module for Apache
Summary(pl):	Modu³ uwierzytelnienia samba dla Apache
Name:		apache1-mod_%{mod_name}
Version:	1.1
Release:	1
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modauthsamba/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	9478a055e5cedd8c00beaed83d324240
Patch0:		%{name}-symbol_fix.patch
URL:		http://modauthsamba.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel
BuildRequires:	gdbm-devel
BuildRequires:	pam-devel
BuildRequires:	pam-pam_smb
Requires(post,preun):	%{apxs}
Requires:	apache1
Requires:	pam-pam_smb
Obsoletes:	apache-mod_%{mod_name} <= %{epoch}:%{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using user entries in an samba directory.

%description -l pl
To jest modu³ uwierzytelnienia dla Apache pozwalaj±cy na
uwierzytelnianie klientów HTTP z u¿yciem wpisów w katalogu samby.

%prep
%setup -q -n mod_%{mod_name}
%patch0 -p1

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so \
	-lgdbm -lcrypt -lpam /%{_lib}/security/pam_smb_auth.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.html
%attr(755,root,root) %{_pkglibdir}/*
