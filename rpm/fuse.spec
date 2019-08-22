Name:       fuse
Summary:    File System in Userspace (FUSE) utilities
Version:    2.9.9
Release:    1
Group:      System/Base
License:    LGPLv2+
URL:        http://fuse.sf.net
Source0:    http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:    %{name}.conf
Patch0:     fuse-udev_rules.patch
Patch1:     fuse-0001-More-parentheses.patch
Patch2:     200-backport_arm64_fuse_kernel_h_clean_includes.patch
Requires:   which
BuildRequires:  gettext-devel

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE userspace tools to
mount a FUSE filesystem.

%package devel
Summary:    File System in Userspace (FUSE) devel files
Group:      Development/Libraries
Requires:   fuse-libs = %{version}-%{release}

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE based applications/filesystems.

%package libs
Summary:    File System in Userspace (FUSE) libraries
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE libraries.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%setup -q -n %{name}-%{version}/%{name}

# fuse-udev_rules.patch
%patch0 -p1
# fuse-0001-More-parentheses.patch
%patch1 -p1
# 200-backport_arm64_fuse_kernel_h_clean_includes.patch
%patch2 -p1

%build
export UDEV_RULES_PATH=/lib/udev/rules.d
./makeconf.sh

%configure --disable-static \
    --bindir=/bin \
    --exec-prefix=/ \
    --enable-example

make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
%make_install

install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf
%ifnarch %{ix86} x86_64
# HACK!!! Please remove when possible.
# For some reason /dev/fuse doesn't exist on ARM builds and make install
# creates the node which doesn't belong to the package, thus these lines.
rm -f %{buildroot}/dev/fuse
rm -rf  %{buildroot}/dev
%endif

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
        AUTHORS ChangeLog NEWS README.md README.NFS

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
/sbin/mount.fuse
%attr(4755,root,root) /bin/fusermount
/bin/ulockmgr_server
%exclude %{_sysconfdir}/init.d/fuse
%config /lib/udev/rules.d/99-fuse.rules
%config(noreplace) %{_sysconfdir}/%{name}.conf

%files devel
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse

%files libs
%defattr(-,root,root,-)
%license COPYING.LIB
%{_libdir}/libfuse.so.*
%{_libdir}/libulockmgr.so.*

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/fusermount.1.gz
%{_mandir}/man1/ulockmgr_server.1.gz
%{_mandir}/man8/mount.fuse.8.gz
%{_docdir}/%{name}-%{version}
