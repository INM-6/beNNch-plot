import bench_plots

hashes = ['4fb0adec2be4b339fa5d376144af67b1b94d850b5258d2991602299e0692fc24',
          '52b69688cf44cb84fc634a8fb391c9d8334384299eaa4ad5e4552142dd441644',
          '65d30ae6f414da80cf5529f8d66fb11f7904b3d52396692ff61e9b448092adff',
          '67a8f7b35e6c1b51e8eb0a908544c5a577f129a548b7f2d0299e79e9fab7a0dc',
          '6d84d54f5faa9fc038fb6bd561f4d2d8e5d1db48bac281f3ad9a360c5d5833da',
          '7c5d48696468de1a4f3c7f058dd5fa43976e1e985a91efd1d3c9783409050d79',
          '9ae2fdebfbbb73caa04561ed056107ff04b3d520dc37378eac7188432a5eb779',
          'a75a2f74507f0ed23d1ba20ad603ea5fc4154353bc053164093bd790d287703b',
          'bd4e0854a2e22f4ca6c80106748eb8e10be98e5320be1919897c6077bcfc725b',
          'c8ef5e016b3ddc9f190001d6522f4c810b77f3e3a78495c0a18f81d1d9b14f33',
          'ef97d01bacc4b7fd11a52a04788321f34bad6d573df42f1e6390ea2cf1369a21']

bench_plots.Bench_Plot(
    data_hash=hashes[0],
    x_axis='num_nvp',
    y_axis=[['sim_factor']],
    x_label='NVP',
    y_label=[r'real-time factor $T_{\textnormal{wall}}'
             r'/T_{\textnormal{model}}$'],
    log_x_axis=True,
    log_y_axis=True,
    data_path='../data_spike_delivery_profiling/',
    catalogue_path='../catalogue.yaml',
    save_path='../plots_spike_delivery2',
    fill_variables=['frac_phase_update',
                    'frac_phase_communicate',
                    'frac_phase_deliver'],
    x_ticks=[1,2,4,8,16,32,64])
