# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	pydoctor
Summary:	API doc generator
Name:		python3-%{module}
Version:	25.10.1
Release:	2
License:	MIT/X11
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pydoctor/
Source0:	https://files.pythonhosted.org/packages/source/p/pydoctor/%{module}-%{version}.tar.gz
# Source0-md5:	c71040b4403b3b84aad37d50f0c17ae8
URL:		https://pypi.org/project/pydoctor/
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-bs4
BuildRequires:	python3-cachecontrol
BuildRequires:	python3-configargparse
BuildRequires:	python3-docutils >= 0.18.1
BuildRequires:	python3-hypothesis
BuildRequires:	python3-lunr
BuildRequires:	python3-pytest
BuildRequires:	python3-twisted
BuildRequires:	sphinx-pdg-3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-lunr
BuildRequires:	python3-sphinx_argparse
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-spelling
BuildRequires:	python3-twisted
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is pydoctor, a standalone API documentation generator that works
by static analysis.

It was written primarily to replace epydoc for the purposes of the
Twisted project as epydoc has difficulties with zope.interface. If you
are looking for a successor to epydoc after moving to Python 3,
pydoctor might be the right tool for your project as well.

pydoctor puts a fair bit of effort into resolving imports and
computing inheritance hierarchies and, as it aims at documenting
Twisted, knows about zope.interface's declaration API and can present
information about which classes implement which interface, and vice
versa.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
# CacheControl filecache in tests writes under $HOME
install -d test-home
export HOME=$(pwd)/test-home
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
# test_utils.TestDevMode expects the suite to run in Python dev mode
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -X dev -m pytest pydoctor/test
%endif

%if %{with doc}
%{__make} -C docs html \
	PYTHONPATH=$PWD \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pydoctor
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/*
%endif
