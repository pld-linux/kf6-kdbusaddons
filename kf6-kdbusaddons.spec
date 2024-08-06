#
# Conditional build:
%bcond_with	tests		# build without tests

# TODO:
# - runtime Requires if any
# - make test not hanging and switch it back on

%define		kdeframever	6.4
%define		qtver		5.15.2
%define		kfname		kdbusaddons
Summary:	Convenience classes for DBus
Name:		kf6-%{kfname}
Version:	6.4.0
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	72cdb5bca87370c69ebda3f986ffe8b1
URL:		http://www.kde.org/
BuildRequires:	Qt6DBus-devel >= %{qtver}
%{?with_tests:BuildRequires:	Qt6Test-devel >= %{qtver}}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6DBus >= %{qtver}
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDBusAddons provides convenience classes on top of QtDBus, as well as
an API to create KDED modules.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6DBus-devel >= %{qtver}
Requires:	cmake >= 3.16
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}6_qt.lang
%defattr(644,root,root,755)
%doc MAINTAINER README.md
%attr(755,root,root) %{_bindir}/kquitapp6
%attr(755,root,root) %{_libdir}/libKF6DBusAddons.so.*.*.*
%ghost %{_libdir}/libKF6DBusAddons.so.6
%{_datadir}/qlogging-categories6/kdbusaddons.categories
%{_datadir}/qlogging-categories6/kdbusaddons.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KDBusAddons
%{_libdir}/libKF6DBusAddons.so
%{_libdir}/cmake/KF6DBusAddons
