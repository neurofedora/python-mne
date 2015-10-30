%global modname mne

Name:           python-%{modname}
Version:        0.10
Release:        1%{?dist}
Summary:        Magnetoencephalography (MEG) and Electroencephalography (EEG)

License:        BSD
URL:            http://martinos.org/mne/
Source0:        https://github.com/mne-tools/mne-python/archive/v%{version}/%{name}-%{version}.tar.gz
#Source1:        https://s3.amazonaws.com/mne-python/datasets/MNE-sample-data-processed.tar.gz
BuildArch:      noarch

%description
This package is designed for sensor- and source-space analysis of M-EEG data,
including frequency-domain and time-frequency analyses and non-parametric
statistics.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
Provides:       bundled(bootstrap)
Provides:       bundled(js-jquery)
Provides:       bundled(js-jquery-ui)
Provides:       bundled(js-d3)
Provides:       bundled(js-mpld3)
BuildRequires:  python2-devel python-nose
BuildRequires:  numpy
# Test deps
BuildRequires:  scipy
BuildRequires:  python-matplotlib
BuildRequires:  python-six
BuildRequires:  python-scikit-learn
BuildRequires:  python-patsy
#BuildRequires:  Mayavi # XXX: GUI needed
BuildRequires:  python-Traits
Requires:       numpy
Requires:       scipy
Requires:       python-matplotlib
Recommends:     python-scikit-learn
Recommends:     python-pandas
Recommends:     python-patsy
Recommends:     python-pillow
Recommends:     h5py
Recommends:     python-statsmodels
# TODO: python3 version
Recommends:     python-Traits

%description -n python2-%{modname}
This package is designed for sensor- and source-space analysis of M-EEG data,
including frequency-domain and time-frequency analyses and non-parametric
statistics.

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
Provides:       bundled(bootstrap)
Provides:       bundled(js-jquery)
Provides:       bundled(js-jquery-ui)
Provides:       bundled(js-d3)
Provides:       bundled(js-mpld3)
BuildRequires:  python3-devel python3-nose
BuildRequires:  python3-numpy
# Test deps
BuildRequires:  python3-scipy
BuildRequires:  python3-matplotlib
BuildRequires:  python3-six
BuildRequires:  python3-scikit-learn
BuildRequires:  python3-patsy
Requires:       python3-numpy
Requires:       python3-scipy
Requires:       python3-matplotlib
Recommends:     python3-scikit-learn
Recommends:     python3-pandas
Recommends:     python3-patsy
Recommends:     python3-pillow
Recommends:     python3-h5py
Recommends:     python3-statsmodels

%description -n python3-%{modname}
This package is designed for sensor- and source-space analysis of M-EEG data,
including frequency-domain and time-frequency analyses and non-parametric
statistics.

Python 3 version.

%prep
%autosetup -n %{modname}-python-%{version}

#cp -p %{SOURCE1} .
#python -c "import mne; mne.datasets.sample.data_path(verbose=True, download=False)"

rm -rf %{py3dir}
mkdir %{py3dir}
cp -a . %{py3dir}
find %{py3dir}/%{modname}/commands/ -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
sed -i '1s|^#!python|#!%{__python3}|' %{py3dir}/bin/mne

%build
%py2_build
pushd %{py3dir}
  %py3_build
popd

%install
%py2_install
pushd %{py3dir}
  %py3_install
popd

%check
export MNE_SKIP_TESTING_DATASET_TESTS=true
export MNE_SKIP_NETWORK_TESTS=1
nosetests-%{python2_version} -v || :
pushd %{py3dir}
  nosetests-%{python3_version} -v || :
popd

%files -n python2-%{modname}
%license LICENSE.txt
%doc README.rst examples AUTHORS.txt
%{_bindir}/%{modname}-%{python2_version}
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}-%{version}*.egg-info/

%files -n python3-%{modname}
%license LICENSE.txt
%doc README.rst examples AUTHORS.txt
%{_bindir}/%{modname}-%{python3_version}
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}*.egg-info/

%changelog
* Fri Oct 30 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.10-1
- Initial package
