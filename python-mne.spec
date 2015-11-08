%global modname mne

Name:           python-%{modname}
Version:        0.10
Release:        2%{?dist}
Summary:        Magnetoencephalography (MEG) and Electroencephalography (EEG) data analysis

# Bundled FieldTrip
# https://github.com/fieldtrip/fieldtrip/blob/master/realtime/src/buffer/python/FieldTrip.py
# Not possible to package because it is matlab package with some plugins

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
Provides:       bundled(python2-FieldTrip)
BuildRequires:  python2-devel python-nose
BuildRequires:  numpy
# Test deps
BuildRequires:  scipy
BuildRequires:  python-matplotlib
BuildRequires:  python-decorator python2-h5io python2-jdcal python2-six python-tempita
BuildRequires:  python-scikit-learn
BuildRequires:  python-patsy
#BuildRequires:  Mayavi # XXX: GUI needed
BuildRequires:  python2-Traits
Requires:       numpy
Requires:       scipy
Requires:       python-matplotlib
Requires:       python-decorator python2-h5io python2-jdcal python2-six python-tempita
Recommends:     python-scikit-learn
Recommends:     python-pandas
Recommends:     python-patsy
Recommends:     python-pillow
Recommends:     h5py
Recommends:     python-statsmodels
Recommends:     python2-Traits

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
Provides:       bundled(python3-FieldTrip)
BuildRequires:  python3-devel python3-nose
BuildRequires:  python3-numpy
# Test deps
BuildRequires:  python3-scipy
BuildRequires:  python3-matplotlib
BuildRequires:  python3-decorator python3-h5io python3-jdcal python3-six python3-tempita
BuildRequires:  python3-scikit-learn
BuildRequires:  python3-patsy
BuildRequires:  python3-Traits
Requires:       python3-numpy
Requires:       python3-scipy
Requires:       python3-matplotlib
Requires:       python3-decorator python3-h5io python3-jdcal python3-six python3-tempita
Recommends:     python3-scikit-learn
Recommends:     python3-pandas
Recommends:     python3-patsy
Recommends:     python3-pillow
Recommends:     python3-h5py
Recommends:     python3-statsmodels
Recommends:     python3-Traits

%description -n python3-%{modname}
This package is designed for sensor- and source-space analysis of M-EEG data,
including frequency-domain and time-frequency analyses and non-parametric
statistics.

Python 3 version.

%prep
%autosetup -c

mv %{modname}-python-%{version} python2

pushd python2/mne/externals/
  # Remove bundled six, jdcal, decorator, tempita, h5io
  # Save bundled FieldTrip (can't find upstream)
  rm -rf six.py jdcal.py decorator.py tempita/ h5io/
  echo > __init__.py
  [ $(find -maxdepth 1 -mindepth 1 | grep -v FieldTrip.py | grep -v __init__.py | wc -l) -eq 0 ] || exit 1
popd

pushd python2/
  # use all six/jdcal/decorator/h5io from system
  # fix API change for jdjcal/jcal2jd
  find -type f -name '*.py' -exec sed -i \
    -e "s/from mne.externals.six/from six/" \
    -e "s/from \.*externals.six/from six/" \
    -e "s/from mne.externals import six/import six/" \
    -e "s/from \.*externals import six/import six/" \
    -e "s/from \.*externals.jdcal/from jdcal/" \
    -e "s/from \.*externals.decorator/from decorator/" \
    -e "s/from \.*externals.h5io/from h5io/" \
    -e "s/from \.*externals.tempita/from tempita/" \
    -e "s/\(jd2jcal(.*)\)/\1[:-1]/" \
    -e "s/\(jcal2jd(.*)\)/\1[-1]/" \
    {} ';'
  sed -i -e "/mne\.externals\.[^']*/d" setup.py
popd

cp -a python2 python3
find python2/%{modname}/commands/ -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'
find python3/%{modname}/commands/ -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

#cp -p %{SOURCE1} .
#python -c "import mne; mne.datasets.sample.data_path(verbose=True, download=False)"

%build
pushd python2
  %py2_build
popd
pushd python3
  %py3_build
popd

%install
pushd python2
  %py2_install
popd
pushd python3
  %py3_install
popd

# Rename binaries
pushd %{buildroot}%{_bindir}
  mv %{modname} python3-%{modname}

  sed -i '1s|^#!python|#!%{__python3}|' python3-%{modname}
  for i in %{modname} %{modname}-3 %{modname}-%{python3_version}
  do
    ln -s python3-%{modname} $i
  done

  cp python3-%{modname} python2-%{modname}

  sed -i '1s|^#!python|#!%{__python2}|' python2-%{modname}
  for i in %{modname}-2 %{modname}-%{python2_version}
  do
    ln -s python2-%{modname} $i
  done
popd

%check
export MNE_SKIP_TESTING_DATASET_TESTS=true
export MNE_SKIP_NETWORK_TESTS=1
pushd python2
  nosetests-%{python2_version} -v || :
popd
pushd python3
  nosetests-%{python3_version} -v || :
popd

%files -n python2-%{modname}
%license python2/LICENSE.txt
%doc python2/README.rst python2/examples python2/AUTHORS.rst
%{_bindir}/%{modname}-2
%{_bindir}/%{modname}-%{python2_version}
%{_bindir}/python2-%{modname}
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}-%{version}*.egg-info/

%files -n python3-%{modname}
%license python3/LICENSE.txt
%doc python3/README.rst python3/examples python3/AUTHORS.rst
%{_bindir}/%{modname}
%{_bindir}/%{modname}-3
%{_bindir}/%{modname}-%{python3_version}
%{_bindir}/python3-%{modname}
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}*.egg-info/

%changelog
* Sun Nov 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.10-2
- /usr/bin/mne uses python3
- fix dependencies around Traits (add py3 version)
- unbundle jdcal/six/decorator/tempita/h5io
- add Provides: bundled(pythonX-FieldTrip)
- More better Summary

* Fri Oct 30 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.10-1
- Initial package
