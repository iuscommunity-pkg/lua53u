Name:           lua
Version:        5.1
Release:        1%{?dist}
Summary:        Powerful light-weight programming language

Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel, ncurses-devel
Provides:       %{name}-devel = %{version}-%{release}

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.


%prep
%setup -q

%build
make %{?_smp_mflags} \
  MYCFLAGS="$RPM_OPT_FLAGS -fPIC" \
  MYLDFLAGS="-Wl,-E" \
  LOADLIB=-DUSE_DLOPEN=1 \
  DLLIB=-ldl \
%ifarch %{ix86} x86_64
  NUMBER="-DLUA_USER_H='\"../etc/luser_number.h\"' -DUSE_FASTROUND" \
%endif
  USERCONF="-DLUA_USERCONFIG='\"../../etc/saconfig.c\"' -DUSE_READLINE" \
  EXTRA_LIBS="-lm -lreadline -lncurses" \
  linux


%install
rm -rf %{buildroot}
make install \
	INSTALL_TOP=%{buildroot}/usr \
	INSTALL_MAN=%{buildroot}%{_mandir}/man1

%check
make test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYRIGHT HISTORY README doc/*.html doc/*.gif
%{_bindir}/lua*
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua*.a
%{_mandir}/man1/lua*.1*


%changelog
* Mon May 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-1
- version bump

* Sun Oct 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 5.0.2-5
- Fix -debuginfo (#165304).
- Cosmetic specfile improvements.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 5.0.2-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 5.0.2-3
- rebuilt

* Sat Feb 12 2005 David Woodhouse <dwmw2@infradead.org> - 5.0.2-2
- Don't use fastround on ppc

* Tue Feb 01 2005 Panu Matilainen <pmatilai@welho.com> - 5.0.2-1
- update to 5.0.2
- remove epoch 0, drop fedora.us release tag

* Mon Nov 17 2003 Oren Tirosh <oren at hishome.net> - 0:5.0-0.fdr.2
- Enable readline support.

* Sat Jun 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:5.0-0.fdr.1
- First build.
