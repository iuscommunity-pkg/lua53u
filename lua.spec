Name:           lua
Version:        5.1.2
Release:        3%{?dist}
Summary:        Powerful light-weight programming language
Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%{version}.tar.gz
Patch0:         lua-5.1.1-autotoolize.patch.gz
Patch1:         lua-5.1.2-multilib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  readline-devel ncurses-devel

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.


%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.


%prep
%setup -q
%patch0 -p1 -E -z .autoxxx
%patch1 -p1 -z .multilib
# fix perms on auto files
chmod u+x autogen.sh config.guess config.sub configure depcomp install-sh missing


%build
%configure --with-readline
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
make %{?_smp_mflags} LIBS="-ldl" luac_LDADD="liblua.la -lm -ldl"
# also remove readline from lua.pc
sed -i 's/-lreadline -lncurses //g' etc/lua.pc


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.{la,a}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYRIGHT HISTORY README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_bindir}/lua*
%{_libdir}/liblua-*.so
%{_mandir}/man1/lua*.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.2-3
- Also use lib64 instead of lib on ia64 and sparc64 

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.2-2
- Fix multilib condlict in luaconf.h (bz 342561)

* Mon Apr  2 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.2-1
- New upstream release 5.1.2
- Fix use of rpath on x86_64

* Fri Jan 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.1-3
- Remove "-lreadline -lncurses" from lua.pc (bz 213895)

* Sun Oct 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.1-2
- Only link /usr/bin/lua with readline / do not link %%{_libdir}/liblua-5.1.so
  with readline so that we don't cause any License troubles for packages
  linking against liblua-5.1.so, otherwise lua could drag the GPL only readline
  lib into the linking of non GPL apps.

* Sat Oct 14 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.1-1
- New upstream release 5.1.1
- Fix detection of readline during compile (iow add readline support back)

* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-7
- Rebuild for FC6

* Thu Jun 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-6
- fixed broken provides

* Tue Jun 06 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-5
- split out devel subpackage

* Thu Jun 01 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-4
- added Requires for pkgconfig BZ#193674

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
