Name:           lua
Version:        5.0
Release:        2
Epoch:          0
Summary:        A powerful light-weight programming language

Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-5.0.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel, ncurses-devel
Provides:       %{name}-devel = %{epoch}:%{version}-%{release}

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
  NUMBER="-DLUA_USER_H='\"../etc/luser_number.h\"' -DUSE_FASTROUND" \
  USERCONF="-DLUA_USERCONFIG='\"../../etc/saconfig.c\"' -DUSE_READLINE" \
  EXTRA_LIBS="-lm -lreadline -lncurses"


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall \
  INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} \
  INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
  INSTALL_INC=$RPM_BUILD_ROOT%{_includedir} \
  INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
  INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1 \
  INSTALL_EXEC="install -pm 755" \
  INSTALL_DATA="install -pm 644"


%check || :
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYRIGHT HISTORY README doc/*.html doc/*.gif
%{_bindir}/lua*
%{_includedir}/l*.h
%{_libdir}/liblua*.a
%{_mandir}/man1/lua*.1*


%changelog
* Mon Nov 17 2003 Oren Tirosh <oren at hishome.net> - 0:5.0-0.fdr.2
- Enable readline support.

* Sat Jun 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:5.0-0.fdr.1
- First build.
