%define major 14
%define asiomajor 1
%define libname %mklibname nghttp2_ %{major}
%define asiolibname %mklibname nghttp2_asio %{asiomajor}
%define develname %mklibname -d nghttp2

Summary: Experimental HTTP/2 client, server and proxy
Name: nghttp2
Version: 1.32.0
Release: 2
License: MIT
Group: System/Libraries
URL: https://nghttp2.org/
Source0: https://github.com/nghttp2/nghttp2/archive/v%{version}.tar.gz
# Needed to avoid confusion between python binary 3.7
# and python library 3.7.0-b4 (both are from the same source...)
Patch0: nghttp2-1.32.0-buildfix.patch
BuildRequires: pkgconfig(cunit)
BuildRequires: pkgconfig(libev)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(libcares)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(jansson)
BuildRequires: pkgconfig(zlib)
BuildRequires: boost-devel
BuildRequires: cmake ninja
BuildRequires: python-cython
BuildRequires: python-setuptools
BuildRequires: ruby bison
BuildRequires: python-sphinx

%description
This package contains the HTTP/2 client, server and proxy programs.

%package -n %{libname}
Summary: A library implementing the HTTP/2 protocol
Group: System/Libraries

%description -n %{libname}
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.

%package -n %{asiolibname}
Summary: Asynchronous I/O library implementing the HTTP/2 protocol
Group: System/Libraries

%description -n %{asiolibname}
libnghttp2 is a library implementing Asynchronous I/O for the
Hypertext Transfer Protocol version 2 (HTTP/2) protocol in C.

%package -n %{develname}
Summary: Files needed for building applications with libnghttp2
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} >= %{version}-%{release}
Suggests: %{asiolibname} >= %{version}-%{release}

%description -n %{develname}
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.

%package -n python-nghttp2
Summary: Python bindings for the NGHTTP2 HTTP/2 library
Group: Development/Python
Requires: %{libname} >= %{version}-%{release}

%description -n python-nghttp2
Python bindings for the NGHTTP2 HTTP/2 library

%prep
%autosetup -p1
%ifarch %{ix86}
# As of boost 1.67.0, clang 7.0.0-331113,
# boost-atomic is partially incompatible with clang
# /usr/include/boost/atomic/detail/ops_gcc_x86_dcas.hpp:163:21: error: address argument to atomic builtin cannot be const-qualified ('const volatile boost::atomics::detail::gcc_dcas_x86::storage_type *' (aka 'const volatile unsigned long long *') invalid)
export CC=gcc
export CXX=g++
%endif

%cmake \
	-DLIBEV_INCLUDE_DIR=%{_includedir}/libev \
	-DENABLE_ASIO_LIB:BOOL=TRUE \
	-DENABLE_APP:BOOL=TRUE \
	-DENABLE_PYTHON_BINDINGS:BOOL=TRUE \
	-G Ninja

%build
%ninja -C build

%check
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}"
%ninja -C build check || :

%install
%ninja_install -C build

# will be installed via %%doc
rm -f "$RPM_BUILD_ROOT%{_datadir}/doc/nghttp2/README.rst"

# workaround for debuginfo shrinking by one byte
# https://bugzilla.redhat.com/show_bug.cgi?id=304121
strip -R .comment --strip-unneeded %{buildroot}%{_libdir}/python*/site-packages/*.so

%files
%{_bindir}/h2load
%{_bindir}/nghttp
%{_bindir}/nghttpd
%{_bindir}/nghttpx
%{_bindir}/deflatehd
%{_bindir}/inflatehd
%{_datadir}/nghttp2
%{_mandir}/man1/h2load.1*
%{_mandir}/man1/nghttp.1*
%{_mandir}/man1/nghttpd.1*
%{_mandir}/man1/nghttpx.1*

%files -n %{libname}
%{_libdir}/libnghttp2.so.%{major}*

%files -n %{asiolibname}
%{_libdir}/libnghttp2_asio.so.%{asiomajor}*

%files -n %{develname}
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%doc README.rst

%files -n python-nghttp2
%{_libdir}/python*/site-packages/*.so
%{_libdir}/python*/site-packages/*.egg-info
