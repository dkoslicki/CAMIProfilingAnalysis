# Check L1 norm performance
metric = 'L1norm'
#for metric in ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)', 'L1norm']:
#metric = 'Sensitivity: TP/(TP+FN)'
vals = []
rank = 'phylum'
for name in names:
    for sample_name in ['CAMI_low_S001']:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if 'genus' in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)


np.mean(vals)

sample_name = 'CAMI_low_S001'
rank = 'genus'
metric = 'Sensitivity: TP/(TP+FN)'

res = []
for name in names:
    vals = []
    for rank in ranks: #['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']:#ranks:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                    if rank in results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)']:
                        if rank in results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)']:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)'][rank]):
                                if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)'][rank]):
                                    prec = float(results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)'][rank])
                                    sens = float(results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)'][rank])
                                    if not np.isnan(prec) and not np.isnan(sens):
                                        vals.append((prec+sens)/2.)
    res.append((name, np.mean(vals)))
res = sorted(res, key=lambda x: x[1], reverse=True)
print(res)




a = ['evil_yalow_0', 'evil_yalow_1', 'evil_yalow_2', 'fervent_sammet_0',
       'fervent_sammet_1', 'fervent_sammet_2', 'modest_babbage_0',
       'modest_babbage_1', 'modest_babbage_2', 'modest_babbage_3',
       'modest_babbage_4', 'modest_babbage_6', 'prickly_fermi_0',
       'prickly_fermi_1', 'prickly_fermi_2']