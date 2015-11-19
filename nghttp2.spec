%define major 14
%define libname %mklibname nghttp2_ %{major}
%define develname %mklibname -d nghttp2

Summary: Experimental HTTP/2 client, server and proxy
Name: nghttp2
Version: 1.4.0
Release: %mkrel 1
License: MIT
Group: System/Libraries
URL: https://nghttp2.org/
Source0: https://github.com/tatsuhiro-t/nghttp2/releases/download/v%{version}/nghttp2-%{version}.tar.xz
Patch0: nghttp2-1.4.0-libev.diff
Patch1: 0001-configure-do-not-enable-hidden-visibility.patch
BuildRequires: pkgconfig(cunit)
BuildRequires: pkgconfig(libev)
BuildRequires: openssl-devel

%description
This package contains the HTTP/2 client, server and proxy programs.

%package -n %{libname}
Summary: A library implementing the HTTP/2 protocol
Group: System/Libraries

%description -n %{libname}
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.

%package -n %{develname}
Summary: Files needed for building applications with libnghttp2
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} >= %{version}-%{release}

%description -n %{develname}
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.

%prep

%setup -q

%patch0 -p1

# Do not enable hidden visibility until the upstream test-suite is ready for
# that.  See https://github.com/tatsuhiro-t/nghttp2/issues/410 for details.
%patch1 -p1
touch aclocal.m4 configure {config.h,Makefile}.in


%build
%configure2_5x \
    --disable-python-bindings \
    --disable-static \
    --without-libxml2 \
    --without-spdylay

# avoid using rpath
sed -i libtool                              \
    -e 's/^runpath_var=.*/runpath_var=/'    \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/'

%make

%check
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}"
make check

%install
%makeinstall

# not needed on Fedora/RHEL
rm -f "$RPM_BUILD_ROOT%{_libdir}/libnghttp2.la"

# will be installed via %%doc
rm -f "$RPM_BUILD_ROOT%{_datadir}/doc/nghttp2/README.rst"

%files
%{_bindir}/h2load
%{_bindir}/nghttp
%{_bindir}/nghttpd
%{_bindir}/nghttpx
%{_datadir}/nghttp2
%{_mandir}/man1/h2load.1*
%{_mandir}/man1/nghttp.1*
%{_mandir}/man1/nghttpd.1*
%{_mandir}/man1/nghttpx.1*

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{!?_licensedir:%global license %%doc}
%license COPYING

%files -n %{develname}
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%doc README.rst



%changelog
* Thu Nov 05 2015 oden <oden> 1.4.0-1.mga6
+ Revision: 897929
- fix some small issues...
- imported package nghttp2

