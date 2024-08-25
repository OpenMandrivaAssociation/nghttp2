%define major 14
%define oldlibname %mklibname nghttp2_ 14
%define libname %mklibname nghttp2
%define develname %mklibname -d nghttp2

Summary: Experimental HTTP/2 client, server and proxy
Name: nghttp2
Version: 1.62.1
Release: 2
License: MIT
Group: System/Libraries
URL: https://nghttp2.org/
Source0: https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz
BuildRequires: pkgconfig(cunit)
BuildRequires: pkgconfig(libev)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(libcares)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(jansson)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libbpf)
BuildRequires: pkgconfig(libnghttp3)
BuildRequires: pkgconfig(systemd)
BuildRequires: boost-devel
BuildRequires: ruby bison
BuildRequires: python-sphinx
BuildSystem: cmake
BuildOption: -DLIBEV_INCLUDE_DIR=%{_includedir}/libev
BuildOption: -DENABLE_APP:BOOL=TRUE
BuildOption: -DENABLE_LIBBPF:BOOL=ON

%description
This package contains the HTTP/2 client, server and proxy programs.

%package -n %{libname}
Summary: A library implementing the HTTP/2 protocol
Group: System/Libraries
# Renamed before 5.0
%rename %{oldlibname}

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

%check
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}"
%ninja -C build check || :

%install -a
# will be installed via %%doc
rm -f "$RPM_BUILD_ROOT%{_datadir}/doc/nghttp2/README.rst"

%files
%{_bindir}/h2load
%{_bindir}/nghttp
%{_bindir}/nghttpd
%{_bindir}/nghttpx
%{_bindir}/deflatehd
%{_bindir}/inflatehd
%{_datadir}/nghttp2
%doc %{_mandir}/man1/h2load.1*
%doc %{_mandir}/man1/nghttp.1*
%doc %{_mandir}/man1/nghttpd.1*
%doc %{_mandir}/man1/nghttpx.1*

%files -n %{libname}
%{_libdir}/libnghttp2.so.%{major}*

%files -n %{develname}
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/nghttp2
%{_libdir}/*.so
%doc README.rst
