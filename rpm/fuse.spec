# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.26
# 

Name:       fuse

# >> macros
# << macros

Summary:    File System in Userspace (FUSE) utilities
Version:    2.9.0
Release:    1
Group:      System/Base
License:    LGPLv2+
URL:        http://fuse.sf.net
Source0:    http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:    %{name}.conf
Source100:  fuse.yaml
Patch0:     fuse-udev_rules.patch
Patch1:     fuse-0001-More-parentheses.patch
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


%prep
%setup -q -n %{name}-%{version}/%{name}

# fuse-udev_rules.patch
%patch0 -p1
# fuse-0001-More-parentheses.patch
%patch1 -p1
# >> setup
# << setup

%build
# >> build pre
export UDEV_RULES_PATH=/lib/udev/rules.d
./makeconf.sh
# << build pre

%configure --disable-static \
    --bindir=/bin \
    --exec-prefix=/ \
    --enable-example

make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/fuse.conf
%ifnarch %{ix86}
# HACK!!! Please remove when possible.
# For some reason /dev/fuse doesn't exist on ARM builds and make install
# creates the node which doesn't belong to the package, thus these lines.
rm %{buildroot}/dev/fuse
rm -r %{buildroot}/dev
%endif
# << install post

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
# >> files
%doc COPYING
/sbin/mount.fuse
%attr(4755,root,root) /bin/fusermount
/bin/ulockmgr_server
%exclude %{_sysconfdir}/init.d/fuse
%config /lib/udev/rules.d/99-fuse.rules
%{_mandir}/man1/fusermount.1.gz
%{_mandir}/man1/ulockmgr_server.1.gz
%{_mandir}/man8/mount.fuse.8.gz
%config(noreplace) %{_sysconfdir}/%{name}.conf
# << files

%files devel
%defattr(-,root,root,-)
# >> files devel
%doc AUTHORS ChangeLog COPYING FAQ Filesystems NEWS README README.NFS
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse
# << files devel

%files libs
%defattr(-,root,root,-)
# >> files libs
%doc COPYING.LIB
%{_libdir}/libfuse.so.*
%{_libdir}/libulockmgr.so.*
# << files libs
