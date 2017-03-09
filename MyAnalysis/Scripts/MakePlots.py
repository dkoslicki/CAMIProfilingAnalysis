import sys
import numpy as np
script_directory = '/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/Scripts'
sys.path.extend([script_directory])
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import AnalyzeData as AD
import time
from os import listdir
from os.path import isfile, join
import copy


# The following is to allow the user to press "c" and have the current figure saved to /tmp/fig.png
# or press "w" to save and close
# To automatically trim the white space, use imagemajick: cd /tmp; ls *.png | xargs -I{} convert {} -trim {}
import matplotlib
if not globals().has_key('__figure'):
    __figure = matplotlib.pyplot.figure


def on_key(event):
    """
     This function will save the current figure to /tmp/fig.png upon pressing 'c'. Pressing 'w' will save the figure to /tmp/fig<timestamp> and close the figure
    """
    print event
    if event.key=='c':
        plt.savefig("/tmp/fig.png",bbox_inches='tight')
    if event.key=='w':
        #plt.savefig("/tmp/Tables/fig" + str(time.time())+".png", bbox_inches=0, dpi=800)
        plt.savefig("/tmp/Tables/fig" + str(time.time())+".png", bbox_inches=0)
        plt.close()
def my_figure():
    fig = __figure()
    fig.canvas.mpl_connect('key_press_event',on_key)
    return fig
matplotlib.pyplot.figure = my_figure


# Get the metric result files.
# Assumes that the results are organized out as follows:
# DescriptionFiles.txt: List of full paths to the *.description files (eg: /path/to/profiling/data/submissions_evaluation/00fda87642a7d7279f31bb65/description.properties
# The directory containing the description file should contain the folders "input" and "output", with "metrics.txt" in "output":
#
# profiling/data/submissions_evaluation/00fda87642a7d7279f31bb65/ <-directory name of one entry of DescriptionFiles.txt
# |--description.properties
# |--input
# |   |--biobox.yaml
# |--output
# |   |--biobox.yaml
# |   |--metrics.txt
#
mac = 'y'
if mac=='y':
    base_dir = '/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/'  # Mac
    description_files = []
    fid = open(base_dir + '/Data/DescriptionFiles.txt','r')  # Mac
    for line in fid:
        description_files.append(line.strip())
    fid.close()
else:
    base_dir = 'C:\\Users\\David\\Dropbox\\Repositories\\firstchallenge_evaluation\\profiling\\MyAnalysis'  # Windows
    description_files = []
    fid = open(base_dir + '\\Data\\DescriptionFiles.txt', 'r')  # Windows
    for line in fid:
        description_files.append(line.strip())
    fid.close()
    description_files_windows = list()
    for item in description_files:
        description_files_windows.append('C:\\Users\\David\\Dropbox\\Repositories\\firstchallenge_evaluation\\profiling\\data\\submissions_evaluation\\' + '\\'.join(item.split('/')[9:11]))
    description_files = description_files_windows

###################################################
# Parse results
# Format is:
# results[method][version][competition][sample_name][truth_type] = metrics_content
# with
# metrics_content[metric][rank] = value
(results, names, competitions, sample_names, truth_types, metrics, ranks) = AD.parse_results(description_files, mac=mac)
profiling_names = names


####################################
# Versions

# Get the versions with multiple names
base_names = list()
for name in names:
    base_name = name.split('_')[0]
    base_names.append(base_name)

base_names_with_mult_vers = list()
for base_name in set(base_names):
    if base_names.count(base_name) > 1:
        base_names_with_mult_vers.append(base_name)

for base_name in base_names_with_mult_vers:
    to_plot = list()
    for name in names:
        if name.split('_')[0] == base_name:
            to_plot.append(name)
    plt.figure()
    AD.plot_versus_rank(results,
                        to_plot,
                     'CAMI_low_S001',
                     'filtered',
                     'L1norm',
                     ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
                     )


for base_name in base_names_with_mult_vers:
    to_plot = list()
    for name in names:
        if name.split('_')[0] == base_name:
            to_plot.append(name)
    plt.figure()
    AD.plot_versus_rank(results,
                        to_plot,
                     'CAMI_high',
                     'filtered',
                     'Sensitivity: TP/(TP+FN)',
                     ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
                     )

for base_name in base_names_with_mult_vers:
    to_plot = list()
    for name in names:
        if name.split('_')[0] == base_name:
            to_plot.append(name)
    plt.figure()
    AD.plot_versus_rank(results,
                        to_plot,
                     'CAMI_high',
                     'filtered',
                     'False Positives',
                     ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
                     )

for base_name in base_names_with_mult_vers:
    to_plot = list()
    for name in names:
        if name.split('_')[0] == base_name:
            to_plot.append(name)
    plt.figure()
    AD.plot_versus_rank(results,
                        to_plot,
                     'CAMI_HIGH_S005',
                     'filtered',
                     'False Positives',
                     ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
                     )

# Get the average variance in parameters for each version at the phylum level
rank = 'phylum'
#rank = 'rank independent'
sample_name = 'CAMI_low_S001'
metric = metrics[1]
print(metric)
var_per_method = []
for base_name in base_names_with_mult_vers:#['DUDes']: #base_names_with_mult_vers:
    to_get = []
    for name in names:
        if name.split('_')[0] == base_name:
            to_get.append(name)
    rank_vals = []
    for name in to_get:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                    if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                        if 'genus' in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                                if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                                    val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                                    rank_vals.append(val)
    print(base_name)
    print('Per version metric value:')
    print(rank_vals)
    var_per_method.append(np.var(rank_vals))
print('average variance in parameters for each version at the phylum level')
print(np.mean(var_per_method))

# DUDes has the highest parameter sensitivity
# family sensitivity, 0.00292 -> std = 0.054
# family precision, 0.00468 -> std = 0.068
# family L1 norm 0.00219 -> std = 0.047
# Unifrac 0.305 -> std = 0.55


################################
# Fix taxonomic ranks
#for rank in ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']:
#    plt.figure()
#    AD.plot_bar_at_rank(results,
#                        results.keys(),
#                        'CAMI_low_S001',
#                        'filtered',
#                        'False Positives',
#                        rank
#                        )
colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
AD.spider_plot(results,
            ['L1norm'],
            ['L1norm'],
            results.keys(),
            'CAMI_low_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.4,.8,1.2,1.6,2.0],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=2)


AD.spider_plot(results,
            ['Precision: TP/(TP+FP)'],
            ['Precision'],
            results.keys(),
            'CAMI_MED_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            [colors[1]],
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)

AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)'],
            ['Sensitivity'],
            results.keys(),
            'CAMI_HIGH_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            [colors[2]],
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)



##############################
# Filtering
plt.figure()
AD.plot_versus_rank(results,
                    results.keys(),
                     'CAMI_high',
                     'filtered',
                     'False Positives',
                     ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
                     )

plt.figure()
AD.plot_versus_rank(results,
                    results.keys(),
                     'CAMI_high',
                     'all',
                     'False Positives',
                     ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
                     )

plt.figure()
AD.plot_bar_at_rank(results,
                    sorted(results.keys()),
                    'CAMI_low_S001',
                    'all',
                    'L1norm',
                    'superkingdom',
                    sort='n',
                    lim=[0,.4])

plt.figure()
AD.plot_bar_at_rank(results,
                    sorted(results.keys()),
                    'CAMI_low_S001',
                    'filtered',
                    'L1norm',
                    'superkingdom',
                    sort='n',
                    lim=[0,.4])

plt.figure()
AD.plot_bar_at_rank(results,
                    sorted(results.keys()),
                    'CAMI_low_S001',
                    'all',
                    'Unifrac',
                    'rank independent',
                    sort='n',
                    lim=[0,16])

plt.figure()
AD.plot_bar_at_rank(results,
                    sorted(results.keys()),
                    'CAMI_low_S001',
                    'filtered',
                    'Unifrac',
                    'rank independent',
                    sort='n',
                    lim=[0,16])

plt.figure()
AD.plot_bar_at_rank(results,
                    sorted(results.keys()),
                    'CAMI_MED_S001',#'CAMI_low_S001',
                    'all',
                    'Sensitivity: TP/(TP+FN)',
                    'superkingdom',
                    sort='n',
                    lim=[0,1])

plt.figure()
AD.plot_bar_at_rank(results,
                    sorted(results.keys()),
                    'CAMI_MED_S001',#'CAMI_low_S001',
                    'filtered',
                    'Sensitivity: TP/(TP+FN)',
                    'superkingdom',
                    sort='n',
                    lim=[0,1])

# Which methods detected any non-bacterial organisms?
for sample in ['CAMI_low_S001', 'CAMI_MED_S001', 'CAMI_MED_S002', 'CAMI_HIGH_S001','CAMI_HIGH_S002','CAMI_HIGH_S003','CAMI_HIGH_S004','CAMI_HIGH_S005']:
    plt.figure()
    AD.plot_bar_at_rank(results,
                        sorted(results.keys()),
                        'CAMI_MED_S001',#'CAMI_low_S001',
                        'all',
                        'Sensitivity: TP/(TP+FN)',
                        'superkingdom',
                        sort='n',
                        lim=[0,1])

# Decrease in metrics filtered vs unfiltered
print('Filtered vs unfiltered performance at the superkingdom level')
for metric in ['Sensitivity: TP/(TP+FN)', 'L1norm', 'Unifrac']:
    filtereds = []
    unfiltereds = []
    for name in names:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name] and 'all' in results[name]['CAMI Challenge'][sample_name]:
                    if metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                        if metric in results[name]['CAMI Challenge'][sample_name]['all']:
                            if 'superkingdom' in results[name]['CAMI Challenge'][sample_name]['filtered'][metric] or metric == 'Unifrac':
                                if 'superkingdom' in results[name]['CAMI Challenge'][sample_name]['all'][metric] or metric == 'Unifrac':
                                    if metric != 'Unifrac':
                                        if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['superkingdom']):
                                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['all'][metric]['superkingdom']):
                                                filtered = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['superkingdom'])
                                                unfiltered = float(results[name]['CAMI Challenge'][sample_name]['all'][metric]['superkingdom'])
                                                filtereds.append(filtered)
                                                unfiltereds.append(unfiltered)
                                    else:
                                        if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['rank independent']):
                                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['all'][metric]['rank independent']):
                                                filtered = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['rank independent'])
                                                unfiltered = float(results[name]['CAMI Challenge'][sample_name]['all'][metric]['rank independent'])
                                                filtereds.append(filtered)
                                                unfiltereds.append(unfiltered)

    print('Filtered mean value for metric %s: %f' % (metric, np.mean(filtereds)))
    print('Unfiltered mean value for metric %s: %f' % (metric, np.mean(unfiltereds)))


################################
# Sensitivity versus specificity etc.


AD.metric1_vs_metric2(results,
                       'CAMI_MED_S001',
                       'filtered',
                       ['phylum', 'class', 'order', 'family', 'genus', 'species'],
                       ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)'],
                       ['Sensitivity', 'Precision'],
                       results.keys(),
                       2,
                       3)

AD.metric1_vs_metric2(results,
                       'CAMI_MED_S002',
                       'filtered',
                       ['phylum', 'class', 'order', 'family', 'genus', 'species'],
                       ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)'],
                       ['Sensitivity', 'Precision'],
                       results.keys(),
                       2,
                       3)

AD.metric1_vs_metric2(results,
                       'CAMI_HIGH_S001',
                       'filtered',
                       ['phylum', 'class', 'order', 'family', 'genus', 'species'],
                       ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)'],
                       ['Sensitivity', 'Precision'],
                       results.keys(),
                       2,
                       3)

# Gustav_s FP
plot_ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
#plt.plot([results['Gustav_s']['CAMI Challenge']['CAMI_HIGH_S001']['filtered']['False Positives'][rank] for rank in plot_ranks], linewidth=2)
plt.plot([results['CLARK']['CAMI Challenge']['CAMI_HIGH_S001']['filtered']['False Positives'][rank] for rank in plot_ranks], linewidth=2)
plt.plot([AD.get_TPs('CAMI_HIGH_S001')[rank] for rank in plot_ranks], linewidth=2)
plt.xticks(range(len(plot_ranks)), plot_ranks, rotation=-45)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.subplots_adjust(bottom=0.3)
plt.xlabel('Rank', fontsize=16)
plt.ylabel('False Positives', fontsize=16)
#plt.legend(['Gustav_s', 'Ground Truth Positives'], loc=2)
plt.legend(['CLARK', 'Ground Truth Positives'], loc=2)
plt.title('CAMI_HIGH_S001' + ", " + 'filtered', fontsize=16)
plt.show()

AD.spider_plot(results,
            ['Precision: TP/(TP+FP)'],
            ['Precision'],
            results.keys(),
            'CAMI_HIGH_S001',
            'filtered',
            ['genus'],
            [[1.,0.,0.]],
            1,
            1,
            grid_points=[.2,.4,.6,.8,1.],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)




################################
# Spider plots at each rank

colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
AD.spider_plot(results,
            ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives'],
            ['Unifrac error', 'Recall', 'L1norm error', 'Precision', 'False Positives'],
            results.keys(),
            'CAMI_low_S001',
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


AD.spider_plot(results,
            ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives'],
            ['Unifrac error', 'Recall', 'L1norm error', 'Precision', 'False Positives'],
            results.keys(),
            'CAMI_low_S001',
            'all',
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

AD.spider_plot(results,
            ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives'],
            ['Unifrac error', 'Recall', 'L1norm error', 'Precision', 'False Positives'],
            results.keys(),
            'CAMI_MED_S001',
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

AD.spider_plot(results,
            ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives'],
            ['Unifrac error', 'Recall', 'L1norm error', 'Precision', 'False Positives'],
            results.keys(),
            'CAMI_medium',
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

AD.spider_plot(results,
            ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives'],
            ['Unifrac error', 'Recall', 'L1norm error', 'Precision', 'False Positives'],
            results.keys(),
            'CAMI_HIGH_S001',
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

AD.spider_plot(results,
            ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives'],
            ['Unifrac error', 'Recall', 'L1norm error', 'Precision', 'False Positives'],
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


#####################
# Who wins at which rank (Tables of rankings)
# Press "w", then trim with: ls fig* | xargs -I{} convert {} -trim {}
colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483],[0.517241,0.448276,0.000000],[0.448276,0.965517,1.000000],[0.620690,0.758621,1.000000],[0.448276,0.379310,0.482759],[0.620690,0.000000,0.000000],[0.000000,0.310345,1.000000],[0.000000,0.275862,0.586207],[0.827586,1.000000,0.000000],[0.724138,0.310345,0.827586],[0.241379,0.000000,0.103448],[0.931034,1.000000,0.689655],[1.000000,0.482759,0.379310],[0.275862,1.000000,0.482759],[0.068966,0.655172,0.379310],[0.827586,0.655172,0.655172]])
name_to_color = dict()
it = 0
for name in results.keys():
    name_to_color[name] = colors[it]
    it+=1

name_to_color[''] = [1,1,1]

table_text = AD.rank_table(results,
           'True Positives',
           'TP',
           'CAMI_low_S001',
           ['phylum', 'class', 'order', 'family', 'genus', 'species'],
           results.keys(),
           'filtered',
           name_to_color,
           metric_label='n',
           table_label='y'
           )
AD.winners(table_text)

all_samples = []
for sample_name in ['CAMI_low_S001', 'CAMI_MED_S001', 'CAMI_HIGH_S001']:
    table_text = AD.rank_table(results,
               'True Positives',
               'True Positives',
               sample_name,
               ['phylum', 'class', 'order', 'family', 'genus', 'species'],
               results.keys(),
               'filtered',
               name_to_color,
               metric_label='n',
               table_label='y'
               )
    for item in AD.winners(table_text):
        all_samples.append(item)
    print(AD.winners(table_text))

winner_winners = []
for name in list(set([x[1] for x in all_samples])):
    indicies = [ind for ind, val in enumerate(all_samples) if val[1] == name]
    if len(indicies) == 3:
        winner_winners.append((sum([all_samples[ind][0] for ind in indicies]), name))

print(sorted(winner_winners))  # total ranks across three samples.

all_samples = []
for sample_name in ['CAMI_low_S001', 'CAMI_MED_S001', 'CAMI_HIGH_S001']:
    table_text = AD.rank_table(results,
               'Sensitivity: TP/(TP+FN)',
               'Sensitivity',
               sample_name,
               ['phylum', 'class', 'order', 'family', 'genus', 'species'],
               results.keys(),
               'filtered',
               name_to_color,
               metric_label='n',
               table_label='y'
               )
    for item in AD.winners(table_text):
        all_samples.append(item)
    print(AD.winners(table_text))

winner_winners = []
for name in list(set([x[1] for x in all_samples])):
    indicies = [ind for ind, val in enumerate(all_samples) if val[1] == name]
    if len(indicies) == 3:
        winner_winners.append((sum([all_samples[ind][0] for ind in indicies]), name))

print(sorted(winner_winners))  # total ranks across three samples.

for item in sorted(winner_winners):
    print("%s (%d)" % (item[1], item[0]))

all_samples = []
for sample_name in ['CAMI_low_S001', 'CAMI_MED_S001', 'CAMI_HIGH_S001']:
    table_text = AD.rank_table(results,
               'Precision: TP/(TP+FP)',
               'Precision',
               sample_name,
               ['phylum', 'class', 'order', 'family', 'genus', 'species'],
               results.keys(),
               'filtered',
               name_to_color,
               metric_label='n',
               table_label='y'
               )
    for item in AD.winners(table_text):
        all_samples.append(item)
    print(AD.winners(table_text))

winner_winners = []
for name in list(set([x[1] for x in all_samples])):
    indicies = [ind for ind, val in enumerate(all_samples) if val[1] == name]
    if len(indicies) == 3:
        winner_winners.append((sum([all_samples[ind][0] for ind in indicies]), name))

print(sorted(winner_winners))  # total ranks across three samples. The top one is "chicken dinner". Get it? Winner winner chicken dinner. Boy am I tired.

for item in sorted(winner_winners):
    print("%s (%d)" % (item[1], item[0]))

all_samples = []
for sample_name in ['CAMI_low_S001', 'CAMI_MED_S001', 'CAMI_HIGH_S001']:
    table_text = AD.rank_table(results,
               'False Positives',
               'False Positives',
               sample_name,
               ['phylum', 'class', 'order', 'family', 'genus', 'species'],
               results.keys(),
               'filtered',
               name_to_color,
               metric_label='n',
               table_label='y'
               )
    for item in AD.winners(table_text):
        all_samples.append(item)
    print(AD.winners(table_text))

winner_winners = []
for name in list(set([x[1] for x in all_samples])):
    indicies = [ind for ind, val in enumerate(all_samples) if val[1] == name]
    if len(indicies) == 3:
        winner_winners.append((sum([all_samples[ind][0] for ind in indicies]), name))

print(sorted(winner_winners))  # total ranks across three samples.

all_samples = []
for sample_name in ['CAMI_low_S001', 'CAMI_MED_S001', 'CAMI_HIGH_S001']:
    table_text = AD.rank_table(results,
               'L1norm',
               'L1norm',
               sample_name,
               ['phylum', 'class', 'order', 'family', 'genus', 'species'],
               results.keys(),
               'filtered',
               name_to_color,
               metric_label='n',
               table_label='y'
               )
    for item in AD.winners(table_text):
        all_samples.append(item)
    print(AD.winners(table_text))

winner_winners = []
for name in list(set([x[1] for x in all_samples])):
    indicies = [ind for ind, val in enumerate(all_samples) if val[1] == name]
    if len(indicies) == 3:
        winner_winners.append((sum([all_samples[ind][0] for ind in indicies]), name))

print(sorted(winner_winners))  # total ranks across three samples.

for item in sorted(winner_winners):
    print("%s (%d)" % (item[1], item[0]))

all_samples = []
for sample_name in ['CAMI_low_S001', 'CAMI_MED_S001', 'CAMI_HIGH_S001']:
    table_text = AD.rank_table(results,
               'Unifrac',
               'Unifrac',
               sample_name,
               ['rank independent'],
               results.keys(),
               'filtered',
               name_to_color,
               metric_label='n',
               table_label='y'
               )
    for item in AD.winners(table_text):
        all_samples.append(item)
    print(AD.winners(table_text))

winner_winners = []
for name in list(set([x[1] for x in all_samples])):
    indicies = [ind for ind, val in enumerate(all_samples) if val[1] == name]
    if len(indicies) == 3:
        winner_winners.append((sum([all_samples[ind][0] for ind in indicies]), name))

print(sorted(winner_winners))  # total ranks across three samples.

for item in sorted(winner_winners):
    print("%s (%d)" % (item[1], item[0]))




##################################################
# Absolute performance plots
colors = np.array([[1.000000,0.000000,0.000000],[0.000000,0.000000,0.0172414],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)'],
            ['Recall', 'Precision'],
            results.keys(),
            'CAMI_low_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8,1],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1,
            normalize_l1='y')

colors = np.array([[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)'],
            ['Recall', '0.5*L1norm error', 'Precision'],
            results.keys(),
            'CAMI_low_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8,1],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='n',
            max_plot=1,
            normalize_l1='y')


AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)'],
            ['Recall', 'L1norm error', 'Precision'],
            results.keys(),
            'CAMI_MED_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8,1],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='n',
            max_plot=1,
            normalize_l1='y')

AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)'],
            ['Recall', 'L1norm error', 'Precision'],
            results.keys(),
            'CAMI_medium',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8,1],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='n',
            max_plot=1,
            normalize_l1='y')

AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)'],
            ['Recall', 'L1norm error', 'Precision'],
            results.keys(),
            'CAMI_HIGH_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8,1],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='n',
            max_plot=1,
            normalize_l1='y')

AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)'],
            ['Recall', 'L1norm error', 'Precision'],
            results.keys(),
            'CAMI_high',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8,1],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='n',
            max_plot=1,
            normalize_l1='y')


######################################################################################
# Compute some statistics

# Relative performance
#  ['False Positives', 'Sensitivity: TP/(TP+FN)', 'False Negatives', 'Precision: TP/(TP+FP)', 'True Positives', 'L1norm', 'Unifrac']
# results[names[0]]['CAMI Challenge']['CAMI_low_S001']['filtered']
print('Relative performance between genus and family')
for metric in ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)', 'L1norm']:
    #metric = 'Sensitivity: TP/(TP+FN)'
    rel_performance = []
    for name in names:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                    if 'genus' in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                        if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['family']):
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['genus']):
                                family = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['family'])
                                genus = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['genus'])
                                rel_performance.append((family-genus)/family)

    print('decrease of %f \pm %f for metric %s' % (np.mean(rel_performance), np.std(rel_performance), metric))

# between family and order
print('Relative performance between family and order')
for metric in ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)', 'L1norm']:
    #metric = 'Sensitivity: TP/(TP+FN)'
    rel_performance = []
    for name in names:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                    if 'genus' in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                        if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['family']):
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['order']):
                                family = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['family'])
                                order = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['order'])
                                rel_performance.append((order-family)/order)

    print('decrease of %f \pm %f for metric %s' % (np.mean(rel_performance), np.std(rel_performance), metric))


# Max sensitivity at genus rank
print('Max genus level sensitivity for low complexity sample')
metric = 'Sensitivity: TP/(TP+FN)'
#for metric in ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)', 'L1norm']:
#metric = 'Sensitivity: TP/(TP+FN)'
vals = []
methods = []
for name in names:
    for sample_name in ['CAMI_low_S001']:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if 'genus' in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['genus']):
                        genus = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric]['genus'])
                        vals.append(genus)
                        methods.append(name)

print('Max %s for sample %s at genus level: %f (method %s)' % (metric, sample_name, np.max(vals), methods[vals.index(np.max(vals))]))


# Mean performance at rank
rank = 'phylum'
print('Mean profiler performance at rank %s' % rank)
for metric in metrics:
    #metric = 'Sensitivity: TP/(TP+FN)'
    metric = 'Unifrac'
    if metric == 'Unifrac':
        rank = 'rank independent'
    vals = []
    for name in names:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                    if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                        if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                            val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                            vals.append(val)
    print('Mean value of %f \pm %f for metric %s at rank %s' % (np.mean(vals), np.std(vals), metric, rank))

# Maximal precision + recall
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


# Median performance at <= family
prec_res = []
sens_res = []
for name in names:
    vals = []
    for rank in ['phylum', 'class', 'order', 'family']: #ranks:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name]: #and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                    if rank in results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)']:
                        if rank in results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)']:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)'][rank]):
                                if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)'][rank]):
                                    prec = float(results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)'][rank])
                                    sens = float(results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)'][rank])
                                    if not np.isnan(prec) and not np.isnan(sens):
                                        prec_res.append(prec)
                                        sens_res.append(sens)

print("Median Precision <=family: %f, (max,min)=(%f,%f)" % (np.mean(prec_res), np.max(prec_res), np.min(prec_res)))
print("Median Recall <=family: %f, (max,min)=(%f,%f)" % (np.mean(sens_res), np.max(sens_res), np.min(sens_res)))

# Median performance at > family
prec_res = []
sens_res = []
for name in names:
    vals = []
    for rank in ['genus', 'species']: #ranks:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name]: #and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                    if rank in results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)']:
                        if rank in results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)']:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)'][rank]):
                                if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)'][rank]):
                                    prec = float(results[name]['CAMI Challenge'][sample_name]['filtered']['Precision: TP/(TP+FP)'][rank])
                                    sens = float(results[name]['CAMI Challenge'][sample_name]['filtered']['Sensitivity: TP/(TP+FN)'][rank])
                                    if not np.isnan(prec) and not np.isnan(sens):
                                        prec_res.append(prec)
                                        sens_res.append(sens)

print("Median Precision >family: %f, (max,min)=(%f,%f)" % (np.mean(prec_res), np.max(prec_res), np.min(prec_res)))
print("Median Recall >family: %f, (max,min)=(%f,%f)" % (np.mean(sens_res), np.max(sens_res), np.min(sens_res)))


#######################################################################################################################
# Binning stuff
###############################################
# Binning results.
# Note, this will add the binning results to each plot. Do not evaluate these if you want *just* the profiling results

#binning_results_dir = "/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/BinnerResults"
#binning_names = ["evil_yalow_2","fervent_sammet_2","modest_babbage_6", "prickly_fermi_0"]
binning_results_dir = "/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/BinnerResults/NewResults/final_profiles/low"
binning_names = ['_'.join(f.split('_')[0:3]) for f in listdir(binning_results_dir) if isfile(join(binning_results_dir, f)) and f.split('_')[-1]=='metrics.txt']
sample = 'CAMI_low_S001'
(results2, names2, competitions2, sample_names2, truth_types2, metrics2, ranks2) = AD.add_binning(binning_results_dir, binning_names, results, sample)
names = set(names)
names.update(names2)
names = list(names)

#binning_results_dir = "/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/BinnerResults/medium"
#binning_names = ['evil_yalow_1','fervent_sammet_0','modest_babbage_1','modest_babbage_2','modest_babbage_4','prickly_fermi_1']
binning_results_dir = "/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/BinnerResults/NewResults/final_profiles/medium"
#binning_names = [f for f in listdir(binning_results_dir) if isfile(join(binning_results_dir, f))]
binning_names = ['_'.join(f.split('_')[0:3]) for f in listdir(binning_results_dir) if isfile(join(binning_results_dir, f)) and f.split('_')[-1]=='metrics.txt']
sample = 'CAMI_medium'
(results2, names2, competitions2, sample_names2, truth_types2, metrics2, ranks2) = AD.add_binning(binning_results_dir, binning_names, results, sample)
names = set(names)
names.update(names2)
names = list(names)

#binning_results_dir = "/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/BinnerResults/high"
#binning_names = ['evil_yalow_0','fervent_sammet_1','modest_babbage_0','modest_babbage_3','prickly_fermi_2']
binning_results_dir = "/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/BinnerResults/NewResults/final_profiles/high"
#binning_names = [f for f in listdir(binning_results_dir) if isfile(join(binning_results_dir, f))]
binning_names = ['_'.join(f.split('_')[0:3]) for f in listdir(binning_results_dir) if isfile(join(binning_results_dir, f)) and f.split('_')[-1]=='metrics.txt']
sample = 'CAMI_high'
(results2, names2, competitions2, sample_names2, truth_types2, metrics2, ranks2) = AD.add_binning(binning_results_dir, binning_names, results, sample)
names = set(names)
names.update(names2)
names = list(names)

# Merge low, medium, high
#binning_names = set()
#for name in list(np.setdiff1d(names, profiling_names)):
#    binning_names.add("_".join(name.split("_")[0:2]))

#binning_anonymous_to_real = {"dreamy_archimedes_0":"metawatt","angry_ardinghelli_0":"PPS+","admiring_curie_3":"metabat","admiring_curie_2":"metabat","admiring_curie_1":"metabat","berserk_euclid_2":"MyCC","berserk_euclid_1":"MyCC","berserk_euclid_0":"MyCC","berserk_hypatia_2":"MetaWatt-3.5","berserk_hypatia_1":"MetaWatt-3.5","berserk_hypatia_0":"MetaWatt-3.5","naughty_carson_2":"MaxBin 2.0","naughty_carson_1":"MaxBin 2.0","naughty_carson_0":"MaxBin 2.0","evil_yalow_2":"taxator-tk 1.3.0e","evil_yalow_1":"taxator-tk 1.3.0e","evil_yalow_0":"taxator-tk 1.3.0e","admiring_curie_0":"metabat","fervent_sammet_2":"taxator-tk 1.4pre1e","fervent_sammet_0":"taxator-tk 1.4pre1e","fervent_sammet_1":"taxator-tk 1.4pre1e","modest_babbage_6":"PhyloPythiaS+","modest_babbage_5":"PhyloPythiaS+","modest_babbage_4":"PhyloPythiaS+","modest_babbage_2":"PhyloPythiaS+","modest_babbage_1":"PhyloPythiaS+","modest_babbage_0":"PhyloPythiaS+","modest_babbage_3":"PhyloPythiaS+","elated_franklin_1":"MetaBAT","elated_franklin_0":"MetaBAT","prickly_fermi_0":"Kraken","prickly_fermi_1":"Kraken","prickly_fermi_2":"Kraken","stoic_albattani_3":"MEGAN","cocky_sammet_0":"CONCOCT (kallisto v0.42.2.1)","cocky_sammet_1":"CONCOCT (kallisto v0.42.2.1)","cocky_sammet_2":"CONCOCT (kallisto v0.42.2.1)","goofy_hypatia_0":"CONCOCT (bowtie2)","goofy_hypatia_1":"CONCOCT (bowtie2)","goofy_hypatia_2":"CONCOCT (bowtie2)","lonely_davinci_0":"MEGAN","lonely_davinci_1":"MEGAN","lonely_davinci_2":"MEGAN","lonely_davinci_3":"MEGAN","lonely_davinci_4":"MEGAN","lonely_davinci_5":"MEGAN","drunk_carson_0":"Kraken","drunk_carson_1":"Kraken","drunk_carson_2":"Kraken"}
binning_anonymous_to_real = {"dreamy_archimedes_0":"metawatt","angry_ardinghelli_0":"PPS+","admiring_curie_3":"metabat","admiring_curie_2":"metabat","admiring_curie_1":"metabat","berserk_euclid_2":"MyCC","berserk_euclid_1":"MyCC","berserk_euclid_0":"MyCC","berserk_hypatia_2":"MetaWatt-3.5","berserk_hypatia_1":"MetaWatt-3.5","berserk_hypatia_0":"MetaWatt-3.5","naughty_carson_2":"MaxBin 2.0","naughty_carson_1":"MaxBin 2.0","naughty_carson_0":"MaxBin 2.0","evil_yalow_2":"taxator-tk 1.3.0e","evil_yalow_1":"taxator-tk 1.3.0e","evil_yalow_0":"taxator-tk 1.3.0e","admiring_curie_0":"metabat","fervent_sammet_2":"taxator-tk 1.4pre1e","fervent_sammet_0":"taxator-tk 1.4pre1e","fervent_sammet_1":"taxator-tk 1.4pre1e","modest_babbage_6":"PhyloPythiaS+","modest_babbage_5":"PhyloPythiaS+","modest_babbage_4":"PhyloPythiaS+","modest_babbage_2":"PhyloPythiaS+","modest_babbage_1":"PhyloPythiaS+","modest_babbage_0":"PhyloPythiaS+","modest_babbage_3":"PhyloPythiaS+","elated_franklin_1":"MetaBAT","elated_franklin_0":"MetaBAT","prickly_fermi_0":"Kraken","prickly_fermi_1":"Kraken","prickly_fermi_2":"Kraken","stoic_albattani_3":"MEGAN","cocky_sammet_0":"CONCOCT (kallisto)","cocky_sammet_1":"CONCOCT (kallisto)","cocky_sammet_2":"CONCOCT (kallisto)","goofy_hypatia_0":"CONCOCT (bowtie2)","goofy_hypatia_1":"CONCOCT (bowtie2)","goofy_hypatia_2":"CONCOCT (bowtie2)","lonely_davinci_0":"MEGAN","lonely_davinci_1":"MEGAN","lonely_davinci_2":"MEGAN","lonely_davinci_3":"MEGAN","lonely_davinci_4":"MEGAN","lonely_davinci_5":"MEGAN","drunk_carson_0":"Kraken","drunk_carson_1":"Kraken","drunk_carson_2":"Kraken"}
binning_names = list(set(binning_anonymous_to_real.values()))
# Let's just include KRAKEN, MEGAN, and PhyloPythias+, taxator-tk
old_keys = copy.copy(results.keys())
for name in old_keys:
    if name not in profiling_names:
        if name in binning_anonymous_to_real and binning_anonymous_to_real[name] in ["MEGAN", "Kraken","taxator-tk 1.4pre1e","taxator-tk 1.3.0e","PhyloPythiaS+"]:
            if binning_anonymous_to_real[name] not in results:
                results[binning_anonymous_to_real[name]] = results.pop(name)
            else:
                results[binning_anonymous_to_real[name]]['CAMI Challenge'] = dict(results[binning_anonymous_to_real[name]]['CAMI Challenge'].items() + results.pop(name)['CAMI Challenge'].items())
        else:
            del results[name]



#for name in binning_anonymous_to_real.keys():
#    if name in results:
#        if binning_anonymous_to_real[name] not in results:
#            results[binning_anonymous_to_real[name]] = results.pop(name)
#        else:
#            results[binning_anonymous_to_real[name]]['CAMI Challenge'] = dict(results[binning_anonymous_to_real[name]]['CAMI Challenge'].items() + results.pop(name)['CAMI Challenge'].items())

###################
# With binning.
# NOTE: RUN THE QUICK HACK add_binning BEFORE EVALUATING THE FOLLOWING TO INCLUDE THE BINNING METHODS
colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])

#Low complexity
AD.spider_plot(results,
            ['L1norm'],
            ['L1norm'],
            results.keys(),
            'CAMI_low_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.4,.8,1.2,1.6,2.0],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=2)

AD.spider_plot(results,
            ['Precision: TP/(TP+FP)'],
            ['Precision'],
            results.keys(),
            'CAMI_low_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            [colors[1]],
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)

AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)'],
            ['Sensitivity'],
            results.keys(),
            'CAMI_low_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            [colors[2]],
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)

#Medium complexity
AD.spider_plot(results,
            ['L1norm'],
            ['L1norm'],
            results.keys(),
            'CAMI_medium',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.4,.8,1.2,1.6,2.0],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=2)

AD.spider_plot(results,
            ['Precision: TP/(TP+FP)'],
            ['Precision'],
            results.keys(),
            'CAMI_medium',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            [colors[1]],
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)

AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)'],
            ['Sensitivity'],
            results.keys(),
            'CAMI_medium',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            [colors[2]],
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)



#High complexity
AD.spider_plot(results,
            ['L1norm'],
            ['L1norm'],
            results.keys(),
            'CAMI_high',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.4,.8,1.2,1.6,2.0],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=2)

AD.spider_plot(results,
            ['Precision: TP/(TP+FP)'],
            ['Precision'],
            results.keys(),
            'CAMI_high',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            [colors[1]],
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)

AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)'],
            ['Sensitivity'],
            results.keys(),
            'CAMI_high',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            [colors[2]],
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='y',
            normalize='n',
            legend_loc=(-.5, 1.1),
            fill='y',
            max_plot=1)

###################################
# Binning/profiling bar charts at a fixed rank
# Performance of binners vs profilers
metric = 'Sensitivity: TP/(TP+FN)'
rank = 'family'
#Profiling averages
vals = []
names_vals = []
#for rank in ranks:
for name in profiling_names:
    temp = []
    for sample_name in sample_names:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)
                        temp.append(val)
    if not np.isnan(np.mean(temp)):
        print(name)
        print(temp)
        names_vals.append((name,np.mean(temp)))
vals = []
for name in binning_names:
    temp = []
    for sample_name in sample_names:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)
                        temp.append(val)
    if not np.isnan(np.mean(temp)):
        print(name)
        print(temp)
        names_vals.append((name,np.mean(temp)))

names_vals_sorted = sorted(names_vals, key=lambda x: x[1], reverse=True)
plt.figure()
pos = range(len(names_vals_sorted))
method_colors = []
for elem in names_vals_sorted:
    if elem[0] in binning_names:
        method_colors.append('blue')
    else:
        method_colors.append('green')
plt.barh(pos, [x[1] for x in names_vals_sorted], align='center', color=method_colors)
plt.yticks(pos, (x[0] for x in names_vals_sorted))
plt.xlabel('Recall')
plt.title('Mean %s level performance' % rank)
bin_patch = mpl.patches.Patch(color='blue', label='Binning method')
prof_patch = mpl.patches.Patch(color='green', label='Profiling method')
plt.legend(handles=[bin_patch, prof_patch])
plt.legend()
plt.show()


# Precision
metric = 'Precision: TP/(TP+FP)'
rank = 'family'
#Profiling averages
vals = []
names_vals = []
#for rank in ranks:
for name in profiling_names:
    temp = []
    for sample_name in sample_names:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)
                        temp.append(val)
    if not np.isnan(np.mean(temp)):
        names_vals.append((name,np.mean(temp)))
vals = []
for name in binning_names:
    temp = []
    for sample_name in sample_names:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)
                        temp.append(val)
    if not np.isnan(np.mean(temp)):
        names_vals.append((name,np.mean(temp)))

names_vals_sorted = sorted(names_vals, key=lambda x: x[1], reverse=True)
plt.figure()
pos = range(len(names_vals_sorted))
method_colors = []
for elem in names_vals_sorted:
    if elem[0] in binning_names:
        method_colors.append('blue')
    else:
        method_colors.append('green')
plt.barh(pos, [x[1] for x in names_vals_sorted], align='center', color=method_colors)
plt.yticks(pos, (x[0] for x in names_vals_sorted))
plt.xlabel('Precision')
plt.title('Mean %s level performance' % rank)
bin_patch = mpl.patches.Patch(color='blue', label='Binning method')
prof_patch = mpl.patches.Patch(color='green', label='Profiling method')
plt.legend(handles=[bin_patch, prof_patch])
plt.legend()
plt.show()


# L1 norm
metric = 'L1norm'
rank = 'family'
#Profiling averages
vals = []
names_vals = []
#for rank in ranks:
for name in profiling_names:
    temp = []
    for sample_name in sample_names:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)
                        temp.append(val)
    if not np.isnan(np.mean(temp)):
        names_vals.append((name,np.mean(temp)))
vals = []
for name in binning_names:
    temp = []
    for sample_name in sample_names:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)
                        temp.append(val)
    if not np.isnan(np.mean(temp)):
        names_vals.append((name,np.mean(temp)))

names_vals_sorted = sorted(names_vals, key=lambda x: x[1], reverse=True)
plt.figure()
pos = range(len(names_vals_sorted))
method_colors = []
for elem in names_vals_sorted:
    if elem[0] in binning_names:
        method_colors.append('blue')
    else:
        method_colors.append('green')
plt.barh(pos, [x[1] for x in names_vals_sorted], align='center', color=method_colors)
plt.yticks(pos, (x[0] for x in names_vals_sorted))
plt.xlabel('L1 norm error')
plt.title('Mean %s level performance' % rank)
bin_patch = mpl.patches.Patch(color='blue', label='Binning method')
prof_patch = mpl.patches.Patch(color='green', label='Profiling method')
plt.legend(handles=[bin_patch, prof_patch])
plt.legend()
plt.show()

# Unifrac
metric = 'Unifrac'
rank = 'rank independent'
#Profiling averages
vals = []
names_vals = []
#for rank in ranks:
for name in profiling_names:
    temp = []
    for sample_name in sample_names:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)
                        temp.append(val)
    if not np.isnan(np.mean(temp)):
        names_vals.append((name,np.mean(temp)))
vals = []
for name in binning_names:
    temp = []
    for sample_name in sample_names:
        if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
            if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                    if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                        val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                        vals.append(val)
                        temp.append(val)
    if not np.isnan(np.mean(temp)):
        names_vals.append((name,np.mean(temp)))

names_vals_sorted = sorted(names_vals, key=lambda x: x[1], reverse=True)
plt.figure()
pos = range(len(names_vals_sorted))
method_colors = []
for elem in names_vals_sorted:
    if elem[0] in binning_names:
        method_colors.append('blue')
    else:
        method_colors.append('green')
plt.barh(pos, [x[1] for x in names_vals_sorted], align='center', color=method_colors)
plt.yticks(pos, (x[0] for x in names_vals_sorted))
plt.xlabel('Unifrac error')
plt.title('Mean performance')
bin_patch = mpl.patches.Patch(color='blue', label='Binning method')
prof_patch = mpl.patches.Patch(color='green', label='Profiling method')
plt.legend(handles=[bin_patch, prof_patch])
plt.legend()
plt.show()


#More statistics
# Mean performance at rank
rank = 'order'
print('Mean profiler performance at rank %s' % rank)
for metric in metrics:
    #metric = 'Sensitivity: TP/(TP+FN)'
    if metric == 'Unifrac':
        rank = 'rank independent'
    vals = []
    for name in profiling_names:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                    if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                        if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                            val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                            vals.append(val)
    print('Mean value of %f \pm %f for metric %s at rank %s' % (np.mean(vals), np.std(vals), metric, rank))

# binner
rank = 'order'
print('Mean binning performance at rank %s' % rank)
for metric in metrics:
    #metric = 'Sensitivity: TP/(TP+FN)'
    if metric == 'Unifrac':
        rank = 'rank independent'
    vals = []
    for name in binning_names:
        for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
            if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                    if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                        if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                            val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                            vals.append(val)
    print('Mean value of %f \pm %f for metric %s at rank %s' % (np.mean(vals), np.std(vals), metric, rank))


# Per metric and binning method performance
print('Mean binning performance averaged over samples and ranks')
for name in binning_names:
    for metric in metrics:
        #metric = 'Sensitivity: TP/(TP+FN)'
        vals = []
        for rank in ranks:
            for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
                if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                    if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                        if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                                val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                                vals.append(val)
        if not np.isnan(np.mean(vals)):
            print('Mean value of %f \pm %f for metric %s at rank %s and method %s' % (np.mean(vals), np.std(vals), metric, rank, name))

############################################################
# Main figure recall and precision
# Per metric and profiling method performance
print('Mean profiling performance of top tools, sensitivity, averaged over all ranks <genus and all samples')
vals = []
for name in ['Quikr', 'TIPP', 'Taxy-Pro_v1']:
    for metric in ['Sensitivity: TP/(TP+FN)']:
        for rank in ['phylum', 'class', 'order', 'family']:
            for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
                if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                    if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                        if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                                val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                                vals.append(val)
if not np.isnan(np.mean(vals)):
    print('Mean value of %f \pm %f for metric %s at ranks above genus top 3 performing tools' % (np.mean(vals), np.std(vals), metric))


print('Mean profiling performance of top tools, sensitivity, averaged over all ranks >=genus and all samples')
vals = []
for name in ['Quikr', 'TIPP', 'Taxy-Pro_v1']:
    for metric in ['Sensitivity: TP/(TP+FN)']:
        for rank in ['genus', 'species']:
            for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
                if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                    if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                        if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                                val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                                vals.append(val)
if not np.isnan(np.mean(vals)):
    print('Mean value of %f \pm %f for metric %s at ranks genus/species top 3 performing tools' % (np.mean(vals), np.std(vals), metric))


print('Mean profiling performance of top tools, precision, averaged over all ranks <genus and all samples')
vals = []
for name in ['CK_v0', 'MetaPhlAn2.0', 'mOTU']:
    for metric in ['Precision: TP/(TP+FP)']:
        for rank in ['phylum', 'class', 'order', 'family']:
            for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
                if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                    if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                        if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                                val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                                vals.append(val)
if not np.isnan(np.mean(vals)):
    print('Mean value of %f \pm %f for metric %s at ranks above genus top 3 performing tools' % (np.mean(vals), np.std(vals), metric))


print('Mean profiling performance of top tools, precision, averaged over all ranks >=genus and all samples')
vals = []
for name in ['CK_v0', 'MetaPhlAn2.0', 'mOTU']:
    for metric in ['Precision: TP/(TP+FP)']:
        for rank in ['genus', 'species']:
            for sample_name in ['CAMI_HIGH_S005', 'CAMI_low_S001', 'CAMI_HIGH_S003', 'CAMI_HIGH_S002', 'CAMI_HIGH_S001', 'CAMI_MED_S001', 'CAMI_high', 'CAMI_medium', 'CAMI_MED_S002', 'CAMI_HIGH_S004']:
                if name in results and 'CAMI Challenge' in results[name] and sample_name in results[name]['CAMI Challenge']:
                    if 'filtered' in results[name]['CAMI Challenge'][sample_name] and metric in results[name]['CAMI Challenge'][sample_name]['filtered']:
                        if rank in results[name]['CAMI Challenge'][sample_name]['filtered'][metric]:
                            if AD.is_number(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank]):
                                val = float(results[name]['CAMI Challenge'][sample_name]['filtered'][metric][rank])
                                vals.append(val)
if not np.isnan(np.mean(vals)):
    print('Mean value of %f \pm %f for metric %s at ranks genus/species top 3 performing tools' % (np.mean(vals), np.std(vals), metric))


############################################################
# Main figure

# Relative performance on high complexity sample, legend in center
colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
AD.spider_plot(results,
            ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives'],
            ['Unifrac error', 'Recall', 'L1norm error', 'Precision', 'False Positives'],
            results.keys(),
            'CAMI_HIGH_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='n',
            normalize='y',
            legend_loc=(-.55, 1.1),
            fill='n',
            max_plot=1,
            font_size=14)

# Relative performance on high complexity sample, legend in upper right
name_dict = dict()
for name in results.keys():
    name_split = name.split('_')
    if name_split[0] == 'Taxy-Pro':
        insert_name = 'T-P'
        if len(name_split) > 1:
            insert_name = insert_name + '_' + name_split[1]
    elif name_split[0] == 'FOCUS':
        insert_name = 'FS'
        if len(name_split) > 1:
            insert_name = insert_name + '_' + name_split[1]
    elif name_split[0] == 'MetaPhlAn2.0':
        insert_name = 'MP2.0'
        if len(name_split) > 1:
            insert_name = insert_name + '_' + name_split[1]
    elif name_split[0] == 'MetaPhyler':
        insert_name = 'MPr'
        if len(name_split) > 1:
            insert_name = insert_name + '_' + name_split[1]
    elif name_split[0] == 'DUDes':
        insert_name = 'D'
        if len(name_split) > 1:
            insert_name = insert_name + '_' + name_split[1]
    else:
        insert_name = name
    name_dict[name] = insert_name

colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
data = AD.spider_plot(results,
            ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives'],
            ['Unifrac error', 'Recall', 'L1norm error', 'Precision', 'False Positives'],
            results.keys(),
            'CAMI_HIGH_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8],
            label_grid='n',
            normalize='y',
            #legend_loc=(.9, 2.2),
            legend_loc=(-.75, 1.25),
            fill='n',
            max_plot=1,
            font_size=14,
            legend_fs=14,
            name_dict=name_dict)

# Recall and precision absolute performance, shaded
colors = np.array([[1.000000,0.000000,0.000000],[0.000000,0.000000,0.0172414],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
data = AD.spider_plot(results,
            ['Sensitivity: TP/(TP+FN)', 'Precision: TP/(TP+FP)'],
            ['Recall', 'Precision'],
            results.keys(),
            'CAMI_low_S001',
            'filtered',
            ['phylum', 'class', 'order', 'family', 'genus', 'species'],
            colors,
            2,
            3,
            grid_points=[.2,.4,.6,.8,1],
            label_grid='y',
            normalize='n',
            #legend_loc=(-.5, 1.1),
            legend_loc=(-.75,1.25),
            fill='y',
            max_plot=1,
            normalize_l1='y',
            font_size=14,
            legend_fs=14,
            name_dict=name_dict)
