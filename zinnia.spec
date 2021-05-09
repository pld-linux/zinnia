#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module
#
Summary:	Online handwriting recognition system with machine learning
Summary(pl.UTF-8):	System rozpoznawania pisma ręcznego z uczeniem maszynowym
Name:		zinnia
Version:	0.06
Release:	14
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/zinnia/%{name}-%{version}.tar.gz
# Source0-md5:	5ed6213e2b879465783087a0cf6d5fa0
# http://zinnia.svn.sourceforge.net/viewvc/zinnia/zinnia/tomoe2s.pl
Source1:	tomoe2s.pl
Source2:	Makefile.tomoe
Patch0:		%{name}-gcc.patch
Patch1:		zinnia-fixes-gcc6-compile.patch
URL:		http://zinnia.sourceforge.net/
BuildRequires:	db-devel
BuildRequires:	libstdc++-devel
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	python-devel
BuildRequires:	rpm-perlprov >= 4.1-13
# uses tomoe XMLs
BuildRequires:	tomoe
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zinnia provides a simple, customizable, and portable dynamic OCR
system for hand-written input, based on Support Vector Machines.

Zinnia simply receives user pen strokes as coordinate data and outputs
the best matching characters sorted by SVM confidence. To maintain
portability, it has no rendering functionality. In addition to
recognition, Zinnia provides a training module capable of creating
highly efficient handwriting recognition models.

This package contains the shared library.

%description -l pl.UTF-8
Zinnia zapewnia prosty, konfigurowalny i przenośny system dynamicznego
OCR do pisma ręcznego, oparty na SVM (Support Vector Machines).

Zinnia odbiera uderzenia pióra jako dane o współrzędnych i przekazuje
na wyjściu najlepiej pasujące znaki posortowane według ufności SVM.
Aby zachować przenośność, nie ma funkcji renderowania. Poza
rozpoznawaniem Zinnia udostępnia moduł trenujący, potrafiący tworzyć
bardzo wydajne modele rozpoznawania pisma ręcznego.

Ten pakiet zawiera bibliotekę współdzieloną.

%package devel
Summary:	Header files for Zinnia library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Zinnia
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use Zinnia.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę Zinnia.

%package static
Summary:	Static Zinnia library
Summary(pl.UTF-8):	Statyczna biblioteka Zinnia
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Zinnia library.

%description static -l pl.UTF-8
Statyczna biblioteka Zinnia.

%package utils
Summary:	Utils for the Zinnia library
Summary(pl.UTF-8):	Programy narzędziowe do biblioteki Zinnia
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils
This package provides utilities for Zinnia library.

%description utils -l pl.UTF-8
Ten pakiet zawiera programy narzędziowe do biblioteki Zinnia.

%package doc
Summary:	Documents for the Zinnia library
Summary(pl.UTF-8):	Dokumentacja do biblioteki Zinnia
Group:		Documentation

%description doc
This package provide documents for Zinnia library.

%description doc -l pl.UTF-8
Ten pakiet zawiera dokumentację do biblioteki Zinnia.

%package -n perl-zinnia
Summary:	Perl bindings for Zinnia
Summary(pl.UTF-8):	Wiązania Perla do biblioteki Zinnia
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-zinnia
This package contains Perl bindings for Zinnia.

%description -n perl-zinnia -l pl.UTF-8
Ten pakiet zawiera wiązania Perla do biblioteki Zinnia.

%package -n python-zinnia
Summary:	Python bindings for zinnia
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki Zinnia
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-zinnia
This package contains Python bindings for Zinnia.

%description -n python-zinnia -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona do biblioteki Zinnia.

%package -n python3-zinnia
Summary:	Python 3 bindings for zinnia
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki Zinnia
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-zinnia
This package contains Python 3 bindings for Zinnia.

%description -n python3-zinnia -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona 3 do biblioteki Zinnia.

%package tomoe
Summary:	Tomoe model files for Zinnia
Summary(pl.UTF-8):	Pliki modelu Tomoe dla biblioteki Zinnia
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description tomoe
This package contains Tomoe model files for Zinnia.

%description tomoe -l pl.UTF-8
Ten pakiet zawiera pliki modelu Tomoe dla biblioteki Zinnia.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__rm} python/zinnia.pyc

cp %{SOURCE1} .
cp %{SOURCE2} .

iconv -f latin1 -t utf8 doc/zinnia.css > doc/zinnia.css.utf8
mv -f doc/zinnia.css.utf8 doc/zinnia.css

%build
%configure

%{__make} \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}"

%{__make} -f Makefile.tomoe build

cd perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} \
	CC="%{__cc}"
	OPTIMIZE="%{rpmcflags}"
cd ..

cd python
CC="%{__cc}" \
CFLAGS="-I.. %{rpmcflags}" \
LDFLAGS="-L../.libs %{rpmldflags}" \
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -f Makefile.tomoe install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C perl pure_install \
	DESTDIR=$RPM_BUILD_ROOT

cd python
%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif


# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_libdir}/libzinnia.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzinnia.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzinnia.so
%{_includedir}/zinnia
%{_includedir}/zinnia.h
%{_pkgconfigdir}/zinnia.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzinnia.a
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zinnia
%attr(755,root,root) %{_bindir}/zinnia_convert
%attr(755,root,root) %{_bindir}/zinnia_learn

%files doc
%defattr(644,root,root,755)
%doc doc/*

%files -n perl-zinnia
%defattr(644,root,root,755)
%{perl_vendorarch}/zinnia.pm
%dir %{perl_vendorarch}/auto/zinnia
%attr(755,root,root) %{perl_vendorarch}/auto/zinnia/zinnia.so

%if %{with python2}
%files -n python-zinnia
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_zinnia.so
%{py_sitedir}/zinnia.py[co]
%{py_sitedir}/zinnia_python-0.0.0-py*.egg-info
%endif

%if %{with python3}
%files -n python3-zinnia
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_zinnia.so
%{py3_sitedir}/zinnia.py[co]
%{py3_sitedir}/zinnia_python-0.0.0-py*.egg-info
%endif

%files tomoe
%defattr(644,root,root,755)
%dir %{_datadir}/zinnia
%dir %{_datadir}/zinnia/model
%dir %{_datadir}/zinnia/model/tomoe
%{_datadir}/zinnia/model/tomoe/handwriting-ja.model
%{_datadir}/zinnia/model/tomoe/handwriting-zh_CN.model
