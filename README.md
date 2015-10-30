- [x] requires_pandas = partial(requires_module, name='pandas', call=_pandas_call)
- [x] requires_sklearn = partial(requires_module, name='sklearn', call=_sklearn_call)
- [x] requires_sklearn_0_15 = partial(requires_module, name='sklearn',
                                      call=_sklearn_0_15_call)
- [ ] requires_mayavi = partial(requires_module, name='mayavi', call=_mayavi_call)
- Fixup after split
- [ ] requires_mne = partial(requires_module, name='MNE-C', call=_mne_call)
- Package mne-c
- [ ] requires_freesurfer = partial(requires_module, name='Freesurfer',
                                    call=_fs_call)
- Package freesurfer
- [ ] requires_neuromag2ft = partial(requires_module, name='neuromag2ft',
                                     call=_n2ft_call)
- Package neuromag2ft
- [ ] requires_fs_or_nibabel = partial(requires_module, name='nibabel or Freesurfer',
                                       call=_fs_or_ni_call)
- Package nibabel
- [ ] requires_tvtk = partial(requires_module, name='TVTK',
                        call='from tvtk.api import tvtk')
- Split Mayavi to subpackages and add python3 version
- [x] requires_statsmodels = partial(requires_module, name='statsmodels',
                               call='import statsmodels')
- [x] requires_patsy = partial(requires_module, name='patsy',
                               call='import patsy')
- [ ] requires_pysurfer = partial(requires_module, name='PySurfer',
                                  call='from surfer import Brain')
- Package pysurfer
- [x] requires_PIL = partial(requires_module, name='PIL',
                             call='from PIL import Image')
- [x] requires_good_network = partial(
          requires_module, name='good network connection',
          call='if int(os.environ.get("MNE_SKIP_NETWORK_TESTS", 0)):\n'
               '    raise ImportError')
- [ ] requires_nitime = partial(requires_module, name='nitime',
                          call='import nitime')
- Package nitime
- [x] requires_traits = partial(requires_module, name='traits',
                                call='import traits')
- [x] requires_h5py = partial(requires_module, name='h5py', call='import h5py')
