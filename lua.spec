%global legacy_major_version 5.1
%global legacy_version %{legacy_major_version}.4
%global major_version 5.2

Name:           lua
Version:        %{major_version}.2
Release:        1%{?dist}
Summary:        Powerful light-weight programming language
Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%{version}.tar.gz
Source1:	http://www.lua.org/ftp/lua-%{legacy_version}.tar.gz
Patch0:         %{name}-%{version}-autotoolize.patch
Patch1:         %{name}-%{version}-idsize.patch
Patch2:         %{name}-%{version}-luac-shared-link-fix.patch
Patch3:		%{name}-%{version}-configure-compat-module.patch
Patch4:         %{name}-%{version}-configure-linux.patch
# Legacy patches for compat-lua-libs
Patch10:        lua-5.1.4-autotoolize.patch
Patch11:        lua-5.1.4-lunatic.patch
Patch12:        lua-5.1.4-idsize.patch
Patch13:        lua-5.1.4-2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  automake autoconf libtool readline-devel ncurses-devel
Provides:       lua(abi) = %{major_version}

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
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.

%package static
Summary:        Static library for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description static
This package contains the static version of liblua for %{name}.

%package -n compat-lua-libs
Version:	%{legacy_version}
Summary:	Powerful light-weight programming language (compat version)
Provides:	lua(abi) = %{legacy_version}
Provides:	lua = %{legacy_version}

%description -n compat-lua-libs
This package contains a compatibility version of lua (%{legacy_version}).

%prep
%setup -q -a 1
mv src/luaconf.h src/luaconf.h.template.in
%patch0 -p1 -E -z .autoxxx
%patch1 -p1 -z .idsize
%patch2 -p1 -z .luac-shared
%patch3 -p1 -z .compat-module
%patch4 -p1 -z .configure-linux
autoreconf -i

# legacy
pushd lua-%{legacy_version}
%patch10 -p1 -E -z .legacy-autoxxx
%patch11 -p0 -z .legacy-lunatic
%patch12 -p1 -z .legacy-idsize
%patch13 -p0 -d src -z .legacy-bugfix2
# fix perms on auto files
chmod u+x autogen.sh config.guess config.sub configure depcomp install-sh missing
popd

%build
%configure --with-readline --with-compat-module
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Autotools give me a headache sometimes.
sed -i 's|@pkgdatadir@|%{_datadir}|g' src/luaconf.h.template

# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
make %{?_smp_mflags} LIBS="-lm -ldl" luac_LDADD="liblua.la -lm -ldl"

# legacy
pushd lua-%{legacy_version}
%configure --with-readline
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
make %{?_smp_mflags} LIBS="-lm -ldl" luac_LDADD="liblua.la -lm -ldl"
popd

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_libdir}/lua/%{major_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lua/%{major_version}

# legacy
pushd lua-%{legacy_version}
cp -a ./src/.libs/liblua-%{legacy_major_version}.so $RPM_BUILD_ROOT%{_libdir}/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/lua/%{legacy_major_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lua/%{legacy_major_version}
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_bindir}/lua
%{_bindir}/luac
%{_libdir}/liblua-5.2.so
%{_mandir}/man1/lua*.1*
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{major_version}
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{major_version}

%files devel
%defattr(-,root,root,-)
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua.so
%{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files -n compat-lua-libs
%doc lua-%{legacy_version}/README 
%{_libdir}/liblua-5.1.so
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{legacy_major_version}
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{legacy_major_version}

%changelog
* Thu Apr 11 2013 Tom Callaway <spot@fedoraproject.org> - 5.2.2-1
- update to 5.2.2
- incorporate Aaron Faanes's changes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 06 2011 Tim Niemueller <tim@niemueller.de> - 5.1.4-9
- Provide lua(abi) = 5.1 for better distro updates later

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Tim Niemueller <tim@niemueller.de> - 5.1.4-7
- Add patch to from lua.org with smaller bugfixes
- sed -i -e 's/5\.1\.3/5.1.4/g' on autotoolize patch, bug #641144

* Fri Jan 28 2011 Tim Niemueller <tim@niemueller.de> - 5.1.4-6
- Add patch to increase IDSIZE for more useful error messages

* Sun May 09 2010 Tim Niemueller <tim@niemueller.de> - 5.1.4-5
- Add patch regarding dlopen flags to support Lunatic (Lua-Python bridge)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Tim Niemueller <tim@niemueller.de> - 5.1.4-2
- Link liblua.so with -lm (math lib), fixes rhbz #499238

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 03 2008 Tim Niemueller <tim@niemueller.de> - 5.1.4-1
- New upstream release 5.1.4

* Mon May 12 2008 Tim Niemueller <tim@niemueller.de> - 5.1.3-6
- Add -static subpackage with static liblua, fixes rh bug #445939

* Sun Apr 13 2008 Tim Niemueller <tim@niemueller.de> - 5.1.3-5
- Provide lua = 5.1, this way add-on packages can easily depend on the Lua
  base version and expect certain paths for packages

* Sat Apr  5 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.3-4
- Not only own $libdir/lua/5.1 and $datadir/lua/5.1 but also $libdir/lua
  and $datadir/lua for proper removal of these dirs upon lua removal

* Fri Mar 14 2008 Tim Niemueller <tim@niemueller.de> - 5.1.3-3
- own $libdir/lua/5.1 and $datadir/lua/5.1. These are the standard package
  search path for Lua. Packaging them properly allows for easy creation of
  Lua addon packages.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.1.3-2
- Autorebuild for GCC 4.3

* Sat Jan 26 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.3-1
- New upstream release 5.1.3

* Mon Nov 26 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.2-4
- Fix libdir in lua.pc being /usr/lib on x86_64 (bz 399101)

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
