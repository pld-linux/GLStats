#
# Conditional build:
%bcond_with	apidocs		# build and package API docs (empty as of 0.3.1)
#
Summary:	Generic OpenGL overlay statistics renderer
Summary(pl.UTF-8):	Ogólna biblioteka do renderowania statystyk na nakładce OpenGL
Name:		GLStats
Version:	0.3.1
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/Eyescale/GLStats/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ed80f815bdfdb714aa6269d35c6bfcc1
Patch0:		%{name}-cmake.patch
Patch1:		%{name}-shared.patch
URL:		https://github.com/Eyescale/GLStats/
BuildRequires:	Eyescale-CMake
BuildRequires:	Lunchbox-devel >= 1.10
BuildRequires:	OpenGL-devel
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 2.8
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
Requires:	Lunchbox >= 1.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Generic OpenGL overlay statistics renderer.

%description -l pl.UTF-8
Ogólna biblioteka do renderowania statystyk na nakładce OpenGL.

%package devel
Summary:	Header files for GLStats library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GLStats
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Lunchbox-devel >= 1.10
Requires:	libstdc++-devel

%description devel
Header files for GLStats library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GLStats.

%package apidocs
Summary:	GLStats API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GLStats
Group:		Documentation

%description apidocs
API documentation for GLStats library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GLStats.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

ln -s %{_datadir}/Eyescale-CMake CMake/common
%{__rm} .gitexternals

%build
install -d build
cd build
%cmake ..

%{__make}

%if %{with apidocs}
doxygen doc/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.md
%attr(755,root,root) %{_libdir}/libGLStats.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLStats.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLStats.so
%{_includedir}/GLStats
%{_pkgconfigdir}/GLStats.pc
%dir %{_datadir}/GLStats
%{_datadir}/GLStats/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
