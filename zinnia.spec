#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
%include	/usr/lib/rpm/macros.perl
Summary:	Online handwriting recognition system with machine learning
Name:		zinnia
Version:	0.06
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/zinnia/%{name}-%{version}.tar.gz
# Source0-md5:	5ed6213e2b879465783087a0cf6d5fa0
# http://zinnia.svn.sourceforge.net/viewvc/zinnia/zinnia/tomoe2s.pl
Source1:	tomoe2s.pl
Source2:	Makefile.tomoe
Patch0:		%{name}-gcc.patch
URL:		http://zinnia.sourceforge.net/
BuildRequires:	db-devel
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	python-devel
BuildRequires:	rpm-perlprov >= 4.1-13
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

This package contains the shared libraries.

%package devel
Summary:	Development files for zinnia
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for developing
applications that use zinnia.

%package utils
Summary:	Utils for the zinnia library
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils
This package provides utilities for zinnia library that use zinnia.

%package static
Summary:	Static zinnia library
Summary(pl.UTF-8):	Statyczna biblioteka zinnia
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static zinnia library.

%description static -l pl.UTF-8
Statyczna biblioteka zinnia.

%package doc
Summary:	Documents for the zinnia library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description doc
This package provide documents for zinnia library that use zinnia.

%package -n perl-zinnia
Summary:	Perl bindings for zinnia
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n perl-zinnia
This package contains perl bindings for zinnia.

%package -n python-zinnia
Summary:	Python bindings for zinnia
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-zinnia
This package contains python bindings for zinnia.

%package tomoe
Summary:	Tomoe model file for zinnia
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description tomoe
This package contains tomoe model files for zinnia.

%prep
%setup -q
%patch0 -p1

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
CFLAGS="-I../ %{rpmcflags}" \
LDFLAGS="-L../.libs %{rpmldflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -f Makefile.tomoe install \
	DESTDIR=$RPM_BUILD_ROOT

cd perl
%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

cd python
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libzinnia.so.*.*.*
%attr(755,root,root) %{_libdir}/libzinnia.so.[0-9]

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzinnia.so
%{_includedir}/zinnia*
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
%dir %{perl_vendorarch}/auto/zinnia
%attr(755,root,root) %{perl_vendorarch}/auto/zinnia/zinnia.so
%{perl_vendorarch}/zinnia.pm

%files -n python-zinnia
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_zinnia.so
%{py_sitedir}/zinnia.py*
%{py_sitedir}/zinnia*.egg-info

%files tomoe
%defattr(644,root,root,755)
%dir %{_datadir}/zinnia
%dir %{_datadir}/zinnia/model
%dir %{_datadir}/zinnia/model/tomoe
%{_datadir}/zinnia/model/tomoe/handwriting-ja.model
%{_datadir}/zinnia/model/tomoe/handwriting-zh_CN.model
