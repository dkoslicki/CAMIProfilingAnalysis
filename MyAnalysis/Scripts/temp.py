if name == 'Common Kmers' and version == '':
    return 'Adam_s_1'
elif name == 'Common Kmers' and version == 'Sensitive Unnormalized':
    return 'Adam_s_2'
elif name == 'commonkmers' and version == 'sjanssen':
    return 'Adam_d'
elif name == 'FOCUS' and version == 'cfk8bd':
    return 'Brian_s_1'
elif name == 'FOCUS' and version == 'cfk7bd':
    return 'Brian_s_2'
elif name == 'FOCUS' and version == 'cfk7d':
    return 'Brian_s_3'
elif name == 'FOCUS' and version == 'cfk7b':
    return 'Brian_s_4'
elif name == 'FOCUS' and version == 'cfk8b':
    return 'Brian_s_5'
elif name == 'FOCUS' and version == 'cfk8d':
    return 'Brian_s_6'
elif name == 'FOCUS' and version == 'sjanssen':
    return 'Brian_d'
elif name == 'DUDes' and version == 'old':
    return 'Cesar_s_2'
elif name == 'DUDes' and version == '':
    return 'Cesar_s_1'
elif name == 'Taxy-Pro' and version == 'sjanssen':
    return 'Donald_d'
elif name == 'Taxy-Pro' and version == '':
    return 'Donald_s'
elif name == 'MetaPhyler' and version == 'V1.25':
    return 'Edd_d'
elif name == 'mOTU' and version == '1.1.1':
    return 'Frank_d'
elif name == 'CLARK' and version == 'v1.1.3':
    return 'Gustav_s'
elif name == 'MetaPhlAn2.0' and version == 'db_v20':
    return 'Hank_d'
elif name == 'TIPP' and version == '1.1':
    return 'Isaac_d'
elif name == 'mpipe' and version == '':
    return 'Jack_s'
elif name == 'Quickr' and version == 'sjanssen':
    return 'Kirk_d'
else:
    output = name
    if version != '':
        output = output + "_".version
    output = output.replace(" ","")
    return output

results2 = dict()
for method in results:
    for version in results[method]:
        name = name_to_anonymous_name(method, version)
        results2[name] = results[method][version]




############################################
# Let's pull off a slice
sample = 'CAMI_low_S001'
truth_type = 'all'
competition = 'CAMI Challenge'
#metric = 'L1norm'
#metric = 'True Positives'
#metric = 'False Negatives'
metric = 'False Positives'
data_slice = []
actual_ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
data_slice.append(['Method']+actual_ranks)
for method in methods:
    for version in results[method].keys():
    #for version in [results[method].keys()[0]]:  # Select just one version
        data_row = []
        data_row.append(method + ' ' + version)
        for rank in actual_ranks:
            value = 'NaN'
            try:
                value_string = results[method][version][competition][sample][truth_type][metric][rank]
            except KeyError:
                value_string = 'NaN'
            if AD.is_number(value_string):
                value = float(value_string)
            data_row.append(value)
        data_slice.append(data_row)

out_file_name = '-'.join([competition, sample, truth_type, metric]) + '.txt'
np.savetxt(os.path.join(base_dir, 'Out', out_file_name), data_slice, delimiter=',', fmt='%s')

AD.ave_over_rank(results['Common Kmers']['']['CAMI Challenge']['CAMI_low_S001']['filtered']['False Positives'])

###########################################
#results[method][version][competition][sample_name][truth_type]


filename='goldstandard_low_1.profile'; paste -d' ' <(paste -d' ' <(for word in \"superkingdom\"\: \"phylum\"\: \"class\"\: \"order\"\: \"family\"\: \"genus\"\: \"species\"\: \"strain\"\:; do echo $word; done) <(for word in superkingdom phylum class order family genus species strain; do echo $word; done | xargs -I{} grep -F -w -c {} $filename)) <(for it in `seq 1 8`; do echo ,; done)



##################################

N = 4
theta = AD.radar_factory(N, frame='polygon')

plot_metrics = ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)']
plot_methods = list(methods)[0:5]

data = spider_data(results, plot_metrics, plot_methods)
spoke_labels = data.pop(0)
spoke_labels = ['1-Unifrac/16', 'Sensitivity', '2-L1norm', 'Precision']


fig = plt.figure(figsize=(9, 9))
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

#colors = ['b', 'r', 'g', 'm', 'y']
#colors = plt.get_cmap('jet')(np.linspace(0, 1.0, len(data[0][1])))
# Use matlab distinguishable_colors
colors = np.array([[0,0,1],[1 ,0 ,0],[0 ,1 ,0],[0 ,0 ,0.172413793103448],[1 ,0.103448275862069 ,0.724137931034483],[1 ,0.827586206896552 ,0],[0 ,0.344827586206897 ,0],[0.517241379310345 ,0.517241379310345 ,1],[0.620689655172414 ,0.310344827586207 ,0.275862068965517],[0 ,1 ,0.758620689655172],[0 ,0.517241379310345 ,0.586206896551724],[0 ,0 ,0.482758620689655]])
# Plot the four cases from the example data on separate axes
for n, (title, case_data) in enumerate(data):
    ax = fig.add_subplot(2, 2, n + 1, projection='radar')
    plt.rgrids([0.2, 0.4, 0.6, 0.8])
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip(case_data, colors):
        ax.plot(theta, d, color=color)
        #ax.fill(theta, d, facecolor=color, alpha=0.25)
    ax.set_varlabels(spoke_labels)

# add legend relative to top-left plot
plt.subplot(2, 2, 1)
labels = tuple(plot_methods)
#legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
#legend = plt.legend(labels, loc=1, labelspacing=0.1)
legend = plt.legend(labels, loc=(1.5, .55), labelspacing=0.1)
plt.setp(legend.get_texts(), fontsize='small')

plt.figtext(0.5, 0.965, 'Metrics averaged over taxonomic rank and over versions',
            ha='center', color='black', weight='bold', size='large')
plt.show()


import matplotlib
if not globals().has_key('__figure'):
    __figure = matplotlib.pyplot.figure

def on_key(event):
    print event
    if event.key=='c':
        #print event.canvas.__dict__#.Copy_to_Clipboard(event=event)
       # print event.canvas._tkphoto.__dict__
        plt.savefig("/tmp/fig.png")
def my_figure():
    fig = __figure()
    fig.canvas.mpl_connect('key_press_event',on_key)
    return fig
matplotlib.pyplot.figure = my_figure


for name in names:
    if 'CAMI Challenge' in results[name]:
        print(results[name]['CAMI Challenge']['CAMI_low_S001']['all']['L1norm']['superkingdom'])


def spider_plot(results,
                metrics,
                metrics_labels,
                method_names,
                sample_name,
                truth_type,
                ranks,
                colors,
                num_rows,
                num_cols,
                grid_points=None,
                label_grid='y',
                normalize='y',
                legend_loc=(-.5, 1.1),
                fill='y',
                max_plot=1):
    #def spider_data2(results, metrics, method_names, sample_name, truth_type, ranks):
    competition = 'CAMI Challenge'
    to_plot_method_names = []
    for method_name in method_names:
        if 'CAMI Challenge' in results[method_name]:
            if sample_name in results[method_name]['CAMI Challenge']:
                if truth_type in results[method_name]['CAMI Challenge'][sample_name]:
                    to_plot_method_names.append(method_name)
    to_plot_method_names.sort()
    data = [to_plot_method_names]
    for rank in ranks:
        values_array = []
        for metric in metrics:
            values = []
            for name in to_plot_method_names:
                if competition in results[name] and sample_name in results[name][competition]:
                    if metric == 'Unifrac':
                        val = results[name][competition][sample_name][truth_type][metric]['rank independent']
                        if AD.is_number(val):
                            val = float(val)
                            #val = 1 - float(val) / 12  # This is the largest unifrac is in the dataset: np.nanmax(np.ndarray.flatten(np.array([np.array(val[1])[:,0] for val in data[0:]])))
                            # I could also set this to 16 (since this is the largest it could possibly be)
                    elif metric == 'L1norm':
                        val = results[name][competition][sample_name][truth_type][metric][rank]
                        if AD.is_number(val):
                            val = float(val)
                            #val = 1 - float(val)/2.  # This is to keep it consistent with "larger is better"
                    else:
                        val = results[name][competition][sample_name][truth_type][metric][rank]
                    if not AD.is_number(val) or float(val)<0:
                        value = np.nan
                    else:
                        value = float(val)
                    values.append(value)
                else:
                    values.append(np.nan)
            values_array.append(values)
        data.append((rank, values_array))

    N = len(to_plot_method_names)
    theta = AD.radar_factory(N, frame='polygon')
    dummy = data.pop(0)
    spoke_labels = to_plot_method_names
    fig = plt.figure()
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
    # Plot the four cases from the example data on separate axes
    for n, (title, case_data) in enumerate(data):
        ax = fig.add_subplot(num_rows, num_cols, n + 1, projection='radar')
        if grid_points:
            if label_grid == 'y':
                plt.rgrids(grid_points)
            else:
                plt.rgrids(grid_points, ('','','','')) ###################### This gets rid of the labels of the grid points since everything is relative
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.07), horizontalalignment='center', verticalalignment='center')
        it = 1
        for d, color in zip(case_data, colors):
            if normalize == 'y':
                max_val = max(d)
                for i in range(len(d)):
                    d[i] = d[i]/max_val
            ax.plot(theta, d,'--', color=color, linewidth=5, dashes=(it,1))
            if fill=='y':
                ax.fill(theta, d, facecolor=color, alpha=0.25)
            ax.set_ylim([0,max_plot])
            ax.set_xlim([0,max_plot])
            it+=1
        ax.set_varlabels(spoke_labels, fontsize=10)

    # add legend relative to top-left plot
    labels = tuple(metrics_labels)
    legend = ax.legend(labels, loc='center left', bbox_to_anchor=legend_loc)
    plt.setp(legend.get_texts(), fontsize='small')
    plt.figtext(0.51, 0.965, sample_name, ha='center', color='black', weight='bold', size='large')
    plt.show()
    return

colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
spider_plot(results,
            ['False Positives', 'Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)', 'L1norm', 'Unifrac'],
            ['False Positives', 'Sensitivity', 'Precision', 'L1norm', 'Unifrac'],
            results.keys(),
            'CAMI_high',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='n',
            normalize='y',
            legend_loc=(-.5, 1.1),
            fill='n',
            max_plot=1)








def metric1_vs_metric2(results,
                       plot_sample_name,
                       truth_type,
                       ranks,
                       metrics,
                       metrics_names,
                       method_names,
                       num_rows,
                       num_cols):
    names_to_plot = list()
    for name in method_names:
        if 'CAMI Challenge' in results[name]:
            names_to_plot.append(name)
    fig, axes = plt.subplots(num_rows, num_cols, sharex=True, sharey=True)
    for n,rank in enumerate(ranks):
        values = []
        good_names = []
        for name in names_to_plot:
            if 'CAMI Challenge' in results[name] and plot_sample_name in results[name]['CAMI Challenge'] and AD.is_number(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metrics[0]][rank]) and AD.is_number(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metrics[1]][rank]):
                if float(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metrics[0]][rank])>=0 and float(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metrics[1]][rank])>=0:
                    good_names.append(name)
        for name in good_names:
            values.append([float(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metrics[0]][rank]), float(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metrics[1]][rank])])

        ax = fig.add_subplot(num_rows, num_cols, n+1, autoscale_on=True, frameon=False)
        for name, value in zip(good_names, values):
            ax.scatter(value[0],value[1])
            ax.annotate(name, (value[0], value[1]))
            ax.plot([0,1],[0,1], 'k')
            ax.set_xlim([0,1])
            ax.set_ylim([0,1])
            ax.set_title(rank, weight='bold')
            if n==0 or n==3:
                ax.set_ylabel(metrics_names[0])
            if n>2:
                ax.set_xlabel(metrics_names[1])
            ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')

    plt.figtext(0.5, 0.965, plot_sample_name + ", " + truth_type, ha='center', color='black', weight='bold', size='large')
    plt.show()
    return

metric1_vs_metric2(results,
                       'CAMI_HIGH_S001',
                       'filtered',
                       ['phylum', 'class', 'order', 'family', 'genus', 'species'],
                       ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)'],
                       ['Sensitivity', 'Precision'],
                       results.keys(),
                       2,
                       3)
import scipy
import scipy.io
import numpy as np
metrics = ['True Positives', 'False Positives', 'Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)', 'L1norm']
methods = ['Adam_s_1', 'Brian_d', 'Hank_d', 'Kirk_d', 'Gustav_s', 'Edd_d']
ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
samples = ['CAMI_low_S001', 'CAMI_MED_S001', 'CAMI_HIGH_S001']
to_print = []
for method in methods:
    samples_results = []
    for sample in samples:
        rank_results = []
        for rank in ranks:
            metric_results = []
            for metric in metrics:
                if AD.is_number(results[method]['CAMI Challenge'][sample]['filtered'][metric][rank]):
                    metric_results.append(float(results[method]['CAMI Challenge'][sample]['filtered'][metric][rank]))
                else:
                    metric_results.append(0)
            rank_results.append(metric_results)
        samples_results.append(rank_results)
    to_print.append(samples_results)

np.savetxt("test.CSV",to_print,delimiter=',')


scipy.io.savemat('test.mat', dict(results=to_print))
