import os, re,sys
import numpy as np
#sys.path.extend(['C:\\Users\\David\\Dropbox\\Repositories\\firstchallenge_evaluation\\profiling\\MyAnalysis\\Scripts'])
sys.path.extend(['/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/Scripts'])
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import AnalyzeData as AD

## The following is to allow the user to press "c" and have the current figure saved to /tmp/fig.png
import matplotlib
if not globals().has_key('__figure'):
    __figure = matplotlib.pyplot.figure

def on_key(event):
    print event
    if event.key=='c':
        #print event.canvas.__dict__#.Copy_to_Clipboard(event=event)
       # print event.canvas._tkphoto.__dict__
        plt.savefig("/tmp/fig.png",bbox_inches='tight')
def my_figure():
    fig = __figure()
    fig.canvas.mpl_connect('key_press_event',on_key)
    return fig
matplotlib.pyplot.figure = my_figure


# Get the metric result files
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



###################################
# Make the data for the spider plot

def spider_data(results, metrics, method_names, sample_names, truth_type):
    competition = 'CAMI Challenge'
    #truth_type = 'filtered'
    sample_tuples = [metrics]
    #sample_names = ['CAMI_low_S001', 'CAMI_HIGH_S001', 'CAMI_MED_S001']
    for sample_name in sample_names:
        values_array = []
        for name in method_names:
            values = []
            for metric in metrics:
                value = 0
                counter = 0
                if competition in results[name] and sample_name in results[name][competition]:
                    if metric == 'Unifrac':
                        val = results[name][competition][sample_name][truth_type][metric]['rank independent']
                        if AD.is_number(val):
                            val = 1 - float(val) / 11.902185  # This is the largest unifrac is in the dataset: np.nanmax(np.ndarray.flatten(np.array([np.array(val[1])[:,0] for val in data[0:]])))
                            # I could also set this to 16 (since this is the largest it could possibly be)
                    elif metric == 'L1norm':
                        if AD.is_number(val):
                            val = 0.5*(2 - float(val))  # This is to keep it consistent with "larger is better"
                    else:
                        val = AD.ave_over_rank(results[name][competition][sample_name][truth_type][metric])  # Average over taxonomic rank
                    if AD.is_number(val):
                        counter += 1
                        if float(val) >= 0:
                            value += float(val)
                        else:  # If the value is negative, assume it was supposed to be zeros
                            value += 0
                if counter != 0:
                    values.append(value/float(counter))
                else:
                    values.append(np.nan)
            values_array.append(values)
        sample_tuples.append((sample_name, values_array))
    return sample_tuples


##########################################
##########
def example_data():
    # The following data is from the Denver Aerosol Sources and Health study.
    # See  doi:10.1016/j.atmosenv.2008.12.017
    #
    # The data are pollution source profile estimates for five modeled
    # pollution sources (e.g., cars, wood-burning, etc) that emit 7-9 chemical
    # species. The radar charts are experimented with here to see if we can
    # nicely visualize how the modeled source profiles change across four
    # scenarios:
    #  1) No gas-phase species present, just seven particulate counts on
    #     Sulfate
    #     Nitrate
    #     Elemental Carbon (EC)
    #     Organic Carbon fraction 1 (OC)
    #     Organic Carbon fraction 2 (OC2)
    #     Organic Carbon fraction 3 (OC3)
    #     Pyrolized Organic Carbon (OP)
    #  2)Inclusion of gas-phase specie carbon monoxide (CO)
    #  3)Inclusion of gas-phase specie ozone (O3).
    #  4)Inclusion of both gas-phase speciesis present...
    data = [
        ['Sulfate', 'Nitrate', 'EC', 'OC1', 'OC2', 'OC3', 'OP', 'CO', 'O3'],
        ('Basecase', [
            [0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00, 0.00],
            [0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00, 0.00],
            [0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00, 0.00],
            [0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00, 0.00],
            [0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00, 0.00]]),
        ('With CO', [
            [0.88, 0.02, 0.02, 0.02, 0.00, 0.05, 0.00, 0.05, 0.00],
            [0.08, 0.94, 0.04, 0.02, 0.00, 0.01, 0.12, 0.04, 0.00],
            [0.01, 0.01, 0.79, 0.10, 0.00, 0.05, 0.00, 0.31, 0.00],
            [0.00, 0.02, 0.03, 0.38, 0.31, 0.31, 0.00, 0.59, 0.00],
            [0.02, 0.02, 0.11, 0.47, 0.69, 0.58, 0.88, 0.00, 0.00]]),
        ('With O3', [
            [0.89, 0.01, 0.07, 0.00, 0.00, 0.05, 0.00, 0.00, 0.03],
            [0.07, 0.95, 0.05, 0.04, 0.00, 0.02, 0.12, 0.00, 0.00],
            [0.01, 0.02, 0.86, 0.27, 0.16, 0.19, 0.00, 0.00, 0.00],
            [0.01, 0.03, 0.00, 0.32, 0.29, 0.27, 0.00, 0.00, 0.95],
            [0.02, 0.00, 0.03, 0.37, 0.56, 0.47, 0.87, 0.00, 0.00]]),
        ('CO & O3', [
            [0.87, 0.01, 0.08, 0.00, 0.00, 0.04, 0.00, 0.00, 0.01],
            [0.09, 0.95, 0.02, 0.03, 0.00, 0.01, 0.13, 0.06, 0.00],
            [0.01, 0.02, 0.71, 0.24, 0.13, 0.16, 0.00, 0.50, 0.00],
            [0.01, 0.03, 0.00, 0.28, 0.24, 0.23, 0.00, 0.44, 0.88],
            [0.02, 0.00, 0.18, 0.45, 0.64, 0.55, 0.86, 0.00, 0.16]])
    ]
    return data

plot_sample_names = ['CAMI_high', 'CAMI_medium']
truth_type = 'filtered'
plot_metrics = ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)']
plot_names = results.keys()
N = len(plot_metrics)
theta = AD.radar_factory(N, frame='polygon')

data = spider_data(results, plot_metrics, plot_names, plot_sample_names, truth_type)
spoke_labels = data.pop(0)
spoke_labels = ['1-Unifrac/16', 'Sensitivity', '2-L1norm', 'Precision']

#fig = plt.figure(figsize=(9, 9))
fig = plt.figure()
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
    #ax.set_ylim([0,1])
    #ax.set_xlim([0,1])

# add legend relative to top-left plot
plt.subplot(2, 2, 1)
labels = tuple(plot_names)
#legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
#legend = plt.legend(labels, loc=1, labelspacing=0.1)
legend = plt.legend(labels, loc=(1.5, .55), labelspacing=0.1)
plt.setp(legend.get_texts(), fontsize='small')

plt.figtext(0.5, 0.965, 'Metrics averaged over taxonomic rank and over versions',
            ha='center', color='black', weight='bold', size='large')

plt.show()



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


# Line plot with y-axis the metric, x-axis the taxonomic rank
def plot_versus_rank(names_to_plot, plot_sample_name, truth_type, metric):
    names_to_plot.sort()
    plot_ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
    for key in names_to_plot:
        if plot_sample_name in results[key]['CAMI Challenge']:
            plt.plot([results[key]['CAMI Challenge'][plot_sample_name][truth_type][metric][rank] for rank in plot_ranks], linewidth=2)
    plt.xticks(range(len(plot_ranks)), plot_ranks, rotation=-45)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.subplots_adjust(bottom=0.3)
    plt.xlabel('Rank', fontsize=16)
    plt.ylabel(metric, fontsize=16)
    plt.legend(names_to_plot, loc=2)
    plt.title(plot_sample_name + ", " + truth_type, fontsize=16)
    plt.show()


#plot_sample_name = 'CAMI_medium'
#plot_sample_name = 'CAMI_low_S001'
plot_sample_name = 'CAMI_high'
#plot_sample_name = 'CAMI_HIGH_S001'
truth_type = 'filtered'
metric = 'False Positives'
#metric = 'Sensitivity: TP/(TP+FN)'
#metric = 'Sensitivity: TP/(TP+FN)'
#for plot_sample_name in sample_names:
#    for metric in metrics:
#        for truth_type in truth_types:
for base_name in base_names_with_mult_vers:
    to_plot = list()
    for name in names:
        if name.split('_')[0] == base_name:
            to_plot.append(name)
    plt.figure()
    plot_versus_rank(to_plot, plot_sample_name, truth_type, metric)


################################
# Fix taxonomic ranks
def plot_bar_at_rank(names_to_plot, plot_sample_name, truth_type, metric, rank):
    values = []
    good_names = []
    for name in names_to_plot:
        if 'CAMI Challenge' in results[name] and plot_sample_name in results[name]['CAMI Challenge'] and AD.is_number(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metric][rank]):
            good_names.append(name)
    for name in good_names:
        values.append(float(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metric][rank]))

    sorted_values = sorted(values)
    sorted_names = [s[1] for s in sorted(zip(values,good_names))]
    plt.bar(range(1,len(sorted_values)+1), sorted_values, align='center')
    plt.xticks(range(1,len(sorted_names)+1), sorted_names, rotation='vertical')
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.subplots_adjust(bottom=0.3)
    plt.xlabel('Method', fontsize=16)
    plt.ylabel(metric, fontsize=16)
    plt.title(plot_sample_name + ", " + rank + ", " + truth_type, fontsize=16)
    plt.show()

#plot_sample_name = 'CAMI_high'
plot_sample_name = 'CAMI_low_S001'
truth_type = 'filtered'
metric = 'False Positives'
#metric = 'L1norm'
for rank in ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']:
    plt.figure()
    plot_bar_at_rank(names, plot_sample_name, truth_type, metric, rank)

plot_sample_name = 'CAMI_low_S001'
truth_type = 'filtered'
metric = 'True Positives'
#metric = 'L1norm'
for rank in ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']:
    plt.figure()
    plot_bar_at_rank(names, plot_sample_name, truth_type, metric, rank)


##############################
# Filtering
plot_sample_name = 'CAMI_low_S001'
#metric = 'L1norm'
#rank = 'superkingdom'
metric = 'Unifrac'
rank = 'rank independent'
names_to_plot = list()
for name in names:
    if 'CAMI Challenge' in results[name]:
        names_to_plot.append(name)
names_to_plot.sort()
for truth_type in truth_types:
    plt.figure()
    values = []
    good_names = []
    for name in names_to_plot:
        if 'CAMI Challenge' in results[name] and plot_sample_name in results[name]['CAMI Challenge'] and AD.is_number(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metric][rank]):
            good_names.append(name)
    for name in good_names:
        values.append(float(results[name]['CAMI Challenge'][plot_sample_name][truth_type][metric][rank]))

    sorted_values = values
    sorted_names = good_names
    plt.bar(range(1,len(sorted_values)+1), sorted_values, align='center')
    plt.xticks(range(1,len(sorted_names)+1), sorted_names, rotation='vertical')
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.subplots_adjust(bottom=0.3)
    plt.xlabel('Method', fontsize=16)
    plt.ylabel(metric, fontsize=16)
    plt.title(plot_sample_name + ", " + rank + ", " + truth_type, fontsize=16)
    #plt.ylim([0, 0.4])  # L1norm
    plt.ylim([0,16])  # Unifrac
    plt.show()

################################
# Sensitivity/specificity etc.

#plot_sample_name = 'CAMI_low_S001'
plot_sample_name = 'CAMI_high'
truth_type = 'filtered'
names_to_plot = list()
for name in names:
    if 'CAMI Challenge' in results[name]:
        names_to_plot.append(name)

fig, axes = plt.subplots(2,3, sharex=True, sharey=True)
for n,rank in enumerate(['phylum', 'class', 'order', 'family', 'genus', 'species']):
    values = []
    good_names = []
    for name in names_to_plot:
        if 'CAMI Challenge' in results[name] and plot_sample_name in results[name]['CAMI Challenge'] and AD.is_number(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Sensitivity: TP/(TP+FN)'][rank]) and AD.is_number(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Precision: TP/(TP+FP)'][rank]):
            if float(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Sensitivity: TP/(TP+FN)'][rank])>=0 and float(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Precision: TP/(TP+FP)'][rank])>=0:
                good_names.append(name)

    for name in good_names:
        values.append([float(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Sensitivity: TP/(TP+FN)'][rank]), float(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Precision: TP/(TP+FP)'][rank])])

    ax = fig.add_subplot(2, 3, n+1, autoscale_on=True, frameon=False)
    for name, value in zip(good_names, values):
        ax.scatter(value[0],value[1])
        ax.annotate(name, (value[0], value[1]))
        ax.plot([0,1],[0,1], 'k')
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        ax.set_title(rank, weight='bold')
        if n==0 or n==3:
            ax.set_ylabel('Precision')
        if n>2:
            ax.set_xlabel('Sensitivity')
        ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')

plt.figtext(0.5, 0.965, plot_sample_name + ", " + truth_type, ha='center', color='black', weight='bold', size='large')
plt.show()
########
# Gustav_s FP
plot_ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
plt.plot([results['Gustav_s']['CAMI Challenge']['CAMI_HIGH_S001']['filtered']['False Positives'][rank] for rank in plot_ranks], linewidth=2)
plt.plot([AD.get_TPs('CAMI_HIGH_S001')[rank] for rank in plot_ranks], linewidth=2)
plt.xticks(range(len(plot_ranks)), plot_ranks, rotation=-45)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.subplots_adjust(bottom=0.3)
plt.xlabel('Rank', fontsize=16)
plt.ylabel('False Positives', fontsize=16)
plt.legend(['Gustav_s', 'Ground Truth Positives'], loc=2)
plt.title('CAMI_HIGH_S001' + ", " + truth_type, fontsize=16)
plt.show()

##########################
# L1norm vs unifrac
plot_sample_name = 'CAMI_HIGH_S001'
#plot_sample_name = 'CAMI_high'
truth_type = 'filtered'
names_to_plot = list()
for name in names:
    if 'CAMI Challenge' in results[name]:
        names_to_plot.append(name)

fig, axes = plt.subplots(2,3, sharex=True, sharey=True)
for n,rank in enumerate(['phylum', 'class', 'order', 'family', 'genus', 'species']):
    values = []
    good_names = []
    for name in names_to_plot:
        if 'CAMI Challenge' in results[name] and plot_sample_name in results[name]['CAMI Challenge'] and AD.is_number(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['L1norm'][rank]) and AD.is_number(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Unifrac']['rank independent']):
            if float(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['L1norm'][rank])>=0 and float(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Unifrac']['rank independent'])>=0:
                good_names.append(name)

    for name in good_names:
        values.append([1-float(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['L1norm'][rank])/2., 1-float(results[name]['CAMI Challenge'][plot_sample_name][truth_type]['Unifrac']['rank independent'])/11.1])

    ax = fig.add_subplot(2, 3, n+1, autoscale_on=True, frameon=False)
    for name, value in zip(good_names, values):
        ax.scatter(value[0],value[1])
        ax.annotate(name, (value[0], value[1]))
        ax.plot([0,1],[0,1], 'k')
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        ax.set_title(rank, weight='bold')
        if n==0 or n==3:
            ax.set_ylabel('1-Unifrac/16')
        if n>2:
            ax.set_xlabel('1-L1norm/2')
        ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')

plt.figtext(0.5, 0.965, plot_sample_name + ", " + truth_type, ha='center', color='black', weight='bold', size='large')
plt.show()


################################
# Spider plots at each rank
###################################
# Make the data for the spider plot

def spider_data(results, metrics, method_names, sample_name, truth_type, ranks):
    competition = 'CAMI Challenge'
    sample_tuples = [metrics]
    for rank in ranks:
        values_array = []
        for name in method_names:
            values = []
            for metric in metrics:
                if competition in results[name] and sample_name in results[name][competition]:
                    if metric == 'Unifrac':
                        val = results[name][competition][sample_name][truth_type][metric]['rank independent']
                        if AD.is_number(val):
                            val = 1 - float(val) / 11.902185  # This is the largest unifrac is in the dataset: np.nanmax(np.ndarray.flatten(np.array([np.array(val[1])[:,0] for val in data[0:]])))
                            # I could also set this to 16 (since this is the largest it could possibly be)
                    elif metric == 'L1norm':
                        val = results[name][competition][sample_name][truth_type][metric][rank]
                        if AD.is_number(val):
                            val = 1 - float(val)/2.  # This is to keep it consistent with "larger is better"
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
        sample_tuples.append((rank, values_array))
    return sample_tuples


ranks = ['phylum', 'class', 'order', 'family', 'genus', 'species']
sample_name = 'CAMI_high'
truth_type = 'filtered'
plot_metrics = ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)']
all_method_names = results.keys()
method_names = []
for method_name in all_method_names:
    if 'CAMI Challenge' in results[method_name]:
        if sample_name in results[method_name]['CAMI Challenge']:
            if truth_type in results[method_name]['CAMI Challenge'][sample_name]:
                method_names.append(method_name)

N = len(plot_metrics)
theta = AD.radar_factory(N, frame='polygon')

data = spider_data(results, plot_metrics, method_names, sample_name, truth_type, ranks)
spoke_labels = data.pop(0)
spoke_labels = ['1-Unifrac/16', 'Sensitivity', '1-L1norm/2', 'Precision']

fig = plt.figure()
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

#colors = ['b', 'r', 'g', 'm', 'y']
#colors = plt.get_cmap('jet')(np.linspace(0, 1.0, len(data[0][1])))
# Use matlab distinguishable_colors
colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
colors = colors[0:len(data[0][1])]
# Plot the four cases from the example data on separate axes
for n, (title, case_data) in enumerate(data):
    ax = fig.add_subplot(3, 2, n + 1, projection='radar')
    plt.rgrids([0.2, 0.4, 0.6, 0.8])
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip(case_data, colors):
        ax.plot(theta, d, color=color)
        #ax.fill(theta, d, facecolor=color, alpha=0.25)
    ax.set_varlabels(spoke_labels)
    ax.set_ylim([0,1])
    ax.set_xlim([0,1])

# add legend relative to top-left plot
plt.subplot(3, 2, 1)
labels = tuple(plot_names)
#legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
#legend = plt.legend(labels, loc=1, labelspacing=0.1)
legend = plt.legend(labels, loc=(1.5, .55), labelspacing=0.1)
plt.setp(legend.get_texts(), fontsize='small')

#plt.figtext(0.5, 0.965, 'Metrics averaged over taxonomic rank and over versions', ha='center', color='black', weight='bold', size='large')
plt.show()

##########################
# Plot single spider

ranks = ['phylum']
sample_name = 'CAMI_high'
truth_type = 'filtered'
plot_metrics = ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)']
all_method_names = results.keys()
method_names = []
for method_name in all_method_names:
    if 'CAMI Challenge' in results[method_name]:
        if sample_name in results[method_name]['CAMI Challenge']:
            if truth_type in results[method_name]['CAMI Challenge'][sample_name]:
                method_names.append(method_name)

N = len(plot_metrics)
theta = AD.radar_factory(N, frame='polygon')

data = spider_data(results, plot_metrics, method_names, sample_name, truth_type, ranks)
spoke_labels = data.pop(0)
spoke_labels = ['1-Unifrac/16', 'Sensitivity', '1-L1norm/2', 'Precision']

fig = plt.figure()
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
colors = colors[0:len(data[0][1])]
# Plot the four cases from the example data on separate axes
for n, (title, case_data) in enumerate(data):
    ax = fig.add_subplot(1, 1, n + 1, projection='radar')
    plt.rgrids([0.2, 0.4, 0.6, 0.8])
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip(case_data, colors):
        ax.plot(theta, d, color=color)
    ax.set_varlabels(spoke_labels)
    ax.set_ylim([0,1])
    ax.set_xlim([0,1])

# add legend relative to top-left plot
labels = tuple(plot_names)
legend = ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5))
plt.setp(legend.get_texts(), fontsize='small')
plt.show()

#############################################
# Relative performance
#
def spider_data2(results, metrics, method_names, sample_name, truth_type, ranks):
    competition = 'CAMI Challenge'
    sample_tuples = [method_names]
    for rank in ranks:
        values_array = []
        for metric in metrics:
            values = []
            for name in method_names:
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
        sample_tuples.append((rank, values_array))
    return sample_tuples

#ranks = ['phylum', 'class', 'order', 'family', 'genus', 'species']
ranks = ['genus']
sample_name = 'CAMI_high'
truth_type = 'filtered'
plot_metrics = ['Unifrac', 'Sensitivity: TP/(TP+FN)', 'L1norm', 'Precision: TP/(TP+FP)', 'False Positives']
labels_to_use = ['Unifrac error', 'Sensitivity', 'L1 norm error', 'Precision', 'False Positives']
all_method_names = results.keys()
method_names = []
for method_name in all_method_names:
    if 'CAMI Challenge' in results[method_name]:
        if sample_name in results[method_name]['CAMI Challenge']:
            if truth_type in results[method_name]['CAMI Challenge'][sample_name]:
                method_names.append(method_name)

method_names.sort()
N = len(method_names)
theta = AD.radar_factory(N, frame='polygon')
data = spider_data2(results, plot_metrics, method_names, sample_name, truth_type, ranks)
spoke_labels = data.pop(0)
spoke_labels = method_names
fig = plt.figure()
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
colors = colors[0:len(data[0][1])]
# Plot the four cases from the example data on separate axes
for n, (title, case_data) in enumerate(data):
    ax = fig.add_subplot(2, 3, n + 1, projection='radar')
    #plt.rgrids([0.2, 0.4, 0.6, 0.8])
    plt.rgrids([0.2, 0.4, 0.6, 0.8], ('','','','')) ###################### This gets rid of the labels of the grid points since everything is relative
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.07),
                 horizontalalignment='center', verticalalignment='center')
    it = 1
    for d, color in zip(case_data, colors):
        # Normalize the data so the maximum value is 1. #################### This makes the values relative. Remove if you want absolute
        max_val = max(d)
        for i in range(len(d)):
            d[i] = d[i]/max_val
        ax.plot(theta, d,'--', color=color, linewidth=5, dashes=(it,1))
        ax.set_ylim([0,1])
        ax.set_xlim([0,1])
        it+=1
    ax.set_varlabels(spoke_labels, fontsize=10)

# add legend relative to top-left plot
labels = tuple(labels_to_use)
#legend = ax.legend(labels, loc='center left', bbox_to_anchor=(1.1, 0.53))
legend = ax.legend(labels, loc='center left', bbox_to_anchor=(-.5, 1.1))
#ax.set_varlabels(spoke_labels)
plt.setp(legend.get_texts(), fontsize='small')
plt.figtext(0.51, 0.965, sample_name, ha='center', color='black', weight='bold', size='large')
plt.show()


#################################
# Fill only some of the spiders. Effect of taxonomic rank, L1 norm
ranks = ['phylum', 'class', 'order', 'family', 'genus', 'species']
#ranks = ['genus']
sample_name = 'CAMI_low_S001'
truth_type = 'filtered'
plot_metrics = ['L1norm']
labels_to_use = ['L1norm']
all_method_names = results.keys()
method_names = []
for method_name in all_method_names:
    if 'CAMI Challenge' in results[method_name]:
        if sample_name in results[method_name]['CAMI Challenge']:
            if truth_type in results[method_name]['CAMI Challenge'][sample_name]:
                method_names.append(method_name)

method_names.sort()
N = len(method_names)
theta = AD.radar_factory(N, frame='polygon')
data = spider_data2(results, plot_metrics, method_names, sample_name, truth_type, ranks)
spoke_labels = data.pop(0)
spoke_labels = method_names
fig = plt.figure()
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
colors = np.array([[0.000000,0.000000,1.000000],[1.000000,0.000000,0.000000],[0.000000,1.000000,0.000000],[0.000000,0.000000,0.172414],[1.000000,0.103448,0.724138],[1.000000,0.827586,0.000000],[0.000000,0.344828,0.000000],[0.517241,0.517241,1.000000],[0.620690,0.310345,0.275862],[0.000000,1.000000,0.758621],[0.000000,0.517241,0.586207],[0.000000,0.000000,0.482759],[0.586207,0.827586,0.310345],[0.965517,0.620690,0.862069],[0.827586,0.068966,1.000000],[0.482759,0.103448,0.413793],[0.965517,0.068966,0.379310],[1.000000,0.758621,0.517241],[0.137931,0.137931,0.034483],[0.551724,0.655172,0.482759],[0.965517,0.517241,0.034483]])
colors = colors[0:len(data[0][1])]
# Plot the four cases from the example data on separate axes
for n, (title, case_data) in enumerate(data):
    ax = fig.add_subplot(2, 3, n + 1, projection='radar')
    #plt.rgrids([0.2, 0.4, 0.6, 0.8])
    plt.rgrids([.4, .8, 1.2, 1.6, 2.0])
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.07),
                 horizontalalignment='center', verticalalignment='center')
    it = 1
    for d, color in zip(case_data, colors):
        # Normalize the data so the maximum value is 1. #################### This makes the values relative. Remove if you want absolute
        #max_val = max(d)
        #for i in range(len(d)):
        #    d[i] = d[i]/max_val
        ax.plot(theta, d,'--', color=color, linewidth=5, dashes=(it,1))
        ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_ylim([0,2])
        ax.set_xlim([0,2])
        it+=1
    ax.set_varlabels(spoke_labels, fontsize=10)

# add legend relative to top-left plot
labels = tuple(labels_to_use)
#legend = ax.legend(labels, loc='center left', bbox_to_anchor=(1.1, 0.53))
legend = ax.legend(labels, loc='center left', bbox_to_anchor=(-.5, 1.1))
#ax.set_varlabels(spoke_labels)
plt.setp(legend.get_texts(), fontsize='small')
plt.figtext(0.51, 0.965, sample_name, ha='center', color='black', weight='bold', size='large')
plt.show()

#################################
# Fill only some of the spiders. Effect of taxonomic rank, Precision
#ranks = ['phylum', 'class', 'order', 'family', 'genus', 'species']
ranks = ['genus', 'species']
sample_name = 'CAMI_MED_S001'
#sample_name = 'CAMI_HIGH_S001'
truth_type = 'filtered'
plot_metrics = ['Precision: TP/(TP+FP)']
labels_to_use = ['Precision']
all_method_names = results.keys()
method_names = []
for method_name in all_method_names:
    if 'CAMI Challenge' in results[method_name]:
        if sample_name in results[method_name]['CAMI Challenge']:
            if truth_type in results[method_name]['CAMI Challenge'][sample_name]:
                method_names.append(method_name)

method_names.sort()
N = len(method_names)
theta = AD.radar_factory(N, frame='polygon')
data = spider_data2(results, plot_metrics, method_names, sample_name, truth_type, ranks)
spoke_labels = data.pop(0)
spoke_labels = method_names
fig = plt.figure()
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
colors = np.array([[1.000000,0.000000,0.000000]])
colors = colors[0:len(data[0][1])]
# Plot the four cases from the example data on separate axes
for n, (title, case_data) in enumerate(data):
    ax = fig.add_subplot(2, 3, n + 1, projection='radar')
    #plt.rgrids([0.2, 0.4, 0.6, 0.8])
    plt.rgrids([.2, .4, .6, .8, 1.0])
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.07),
                 horizontalalignment='center', verticalalignment='center')
    it = 1
    for d, color in zip(case_data, colors):
        # Normalize the data so the maximum value is 1. #################### This makes the values relative. Remove if you want absolute
        #max_val = max(d)
        #for i in range(len(d)):
        #    d[i] = d[i]/max_val
        ax.plot(theta, d,'--', color=color, linewidth=5, dashes=(it,1))
        ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_ylim([0,1])
        ax.set_xlim([0,1])
        it+=1
    ax.set_varlabels(spoke_labels, fontsize=10)

# add legend relative to top-left plot
labels = tuple(labels_to_use)
#legend = ax.legend(labels, loc='center left', bbox_to_anchor=(1.1, 0.53))
legend = ax.legend(labels, loc='center left', bbox_to_anchor=(-.5, 1.1))
#ax.set_varlabels(spoke_labels)
plt.setp(legend.get_texts(), fontsize='small')
plt.figtext(0.51, 0.965, sample_name, ha='center', color='black', weight='bold', size='large')
plt.show()

#################################
# Fill only some of the spiders. Effect of taxonomic rank, Sensitivity
ranks = ['phylum', 'class', 'order', 'family', 'genus', 'species']
#ranks = ['genus', 'species']
sample_name = 'CAMI_HIGH_S001'
truth_type = 'filtered'
plot_metrics = ['Sensitivity: TP/(TP+FN)']
labels_to_use = ['Sensitivity']
all_method_names = results.keys()
method_names = []
for method_name in all_method_names:
    if 'CAMI Challenge' in results[method_name]:
        if sample_name in results[method_name]['CAMI Challenge']:
            if truth_type in results[method_name]['CAMI Challenge'][sample_name]:
                method_names.append(method_name)

method_names.sort()
N = len(method_names)
theta = AD.radar_factory(N, frame='polygon')
data = spider_data2(results, plot_metrics, method_names, sample_name, truth_type, ranks)
spoke_labels = data.pop(0)
spoke_labels = method_names
fig = plt.figure()
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
colors = np.array([[0.000000,1.000000,0.000000]])
colors = colors[0:len(data[0][1])]
# Plot the four cases from the example data on separate axes
for n, (title, case_data) in enumerate(data):
    ax = fig.add_subplot(2, 3, n + 1, projection='radar')
    #plt.rgrids([0.2, 0.4, 0.6, 0.8])
    plt.rgrids([.2, .4, .6, .8, 1.0])
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.07),
                 horizontalalignment='center', verticalalignment='center')
    it = 1
    for d, color in zip(case_data, colors):
        # Normalize the data so the maximum value is 1. #################### This makes the values relative. Remove if you want absolute
        #max_val = max(d)
        #for i in range(len(d)):
        #    d[i] = d[i]/max_val
        ax.plot(theta, d,'--', color=color, linewidth=5, dashes=(it,1))
        ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_ylim([0,1])
        ax.set_xlim([0,1])
        it+=1
    ax.set_varlabels(spoke_labels, fontsize=10)

# add legend relative to top-left plot
labels = tuple(labels_to_use)
#legend = ax.legend(labels, loc='center left', bbox_to_anchor=(1.1, 0.53))
legend = ax.legend(labels, loc='center left', bbox_to_anchor=(-.5, 1.1))
#ax.set_varlabels(spoke_labels)
plt.setp(legend.get_texts(), fontsize='small')
plt.figtext(0.51, 0.965, sample_name, ha='center', color='black', weight='bold', size='large')
plt.show()

