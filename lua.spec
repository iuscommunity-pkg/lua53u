Name:           lua
Version:        5.1
Release:        3%{?dist}
Summary:        Powerful light-weight programming language

Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%{version}.tar.gz
Patch0:		lua-5.1-autotoolize-r1.patch.bz2
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
%patch0 -p1

%build
# fix perms on auto files
chmod u+x autogen.sh config.guess config.sub configure depcomp install-sh missing

./autogen.sh

%configure --with-readline

make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
%makeinstall 

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYRIGHT HISTORY README doc/*.html doc/*.gif
%{_bindir}/lua*
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua*.*
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/lua*.1*


%changelog
* Mon May 29 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-3
- added autotools patch from Petri Lehtinen, http://lua-users.org

* Mon May 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-2
- fixed x86_64 builds

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
