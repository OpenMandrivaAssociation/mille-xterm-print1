%define major 1
%define libname %mklibname mille-xterm-print %{major}

%define svn 2137

Summary:	Printer filters for the MILLE-XTERM project
Name:		mille-xterm-print%{major}
Version:	1.0
Release:	%mkrel 0.%{svn}.1
License:	GPL
Group:		System/Servers
URL:		http://www.revolutionlinux.com/mille-xterm
Source:		mille-xterm-print%{major}-%{version}.tar.bz2
BuildRequires:	libcups-devel
BuildRequires:	glib2-devel

%description
This program hides printers from cups. It is used to restrict the visibility
of printers per user, group or physical location.

%package -n	%{libname}
Summary:	Printer filters for the MILLE-XTERM project
Group:		System/Libraries

%description -n %{libname}
This program hides printers from cups. It is used to restrict the visibility
of printers per user, group or physical location.

%package	showprinters
Summary:	Utility to test mille-xterm-print
Group:		System/Servers

%description	showprinters
This program tests which printers are visible to the user when
running under the libhideprinters.so library. It reproduces exactly the
(broken) behavior of Mozilla 1.0.

%package	lpr
Summary:	Mille-Xterm lpr replacement
Group:		System/Servers
Provides:	mille-xterm-print1

%description	lpr
This program replaces lpr and lp: it uses lpr-cups as a backend, but will
launch gtklp if no printer has been selected.

%prep

%setup -q -n %{name}-%{version}

perl -pi -e "s|/lib\b|/%{_lib}|g" src/libhideprinters/*

%build 

cd src/libhideprinters/
%make CC="gcc %{optflags} -Wall -fPIC"

%install
rm -fr %{buildroot}

pushd src/libhideprinters/
%makeinstall
popd

install -d %{buildroot}%{_bindir}
install -m0755 src/lpr-wrapper %{buildroot}%{_bindir}/

%post lpr
# Set up update-alternatives entries
update-alternatives --install %{_bindir}/lpr lpr %{_bindir}/lpr-wrapper 25 --slave %{_mandir}/man1/lpr.1.bz2 lpr.1.bz2 %{_mandir}/man1/lpr-cups.1.bz2
update-alternatives --install %{_bindir}/lp lp %{_bindir}/lpr-wrapper 25 --slave %{_mandir}/man1/lp.1.bz2 lp.1.bz2 %{_mandir}/man1/lp-cups.1.bz2

%preun lpr
if [ "$1" = 0 ]; then
    # Remove update-alternatives entries
    update-alternatives --remove lpr %{_bindir}/lpr-wrapper
    update-alternatives --remove lp %{_bindir}/lpr-wrapper
fi

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc src/libhideprinters/ChangeLog src/libhideprinters/doc/* src/libhideprinters/README src/libhideprinters/TESTING src/libhideprinters/TODO
%{_sysconfdir}/profile.d/*
%{_libdir}/libhideprinters.*

%files showprinters
%defattr(-,root,root)
%doc src/libhideprinters/TESTING
%{_bindir}/showprinters

%files lpr
%defattr(-,root,root)
%{_bindir}/lpr-wrapper


