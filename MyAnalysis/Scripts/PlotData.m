%Run in Scripts folder
%filename = 'CAMI Challenge-CAMI_low_S001-all-L1norm.txt';
filename = 'CAMI Challenge-CAMI_low_S001-all-True Positives.txt';
%filename = 'CAMI Challenge-CAMI_low_S001-all-False Negatives.txt';
%filename = 'CAMI Challenge-CAMI_low_S001-all-False Positives.txt';
full_filename = sprintf('/Users/dkoslicki/Dropbox/Repositories/firstchallenge_evaluation/profiling/MyAnalysis/Out/%s',filename);
[methods,superkingdom,phylum,class,order,family,genus,species,strain] = importfile(full_filename);
[~,ordering] = sort(order,'descend');
data = [superkingdom,phylum,class,order,family,genus,species]';
%data = [phylum,class,order,family,genus,species]';
colors = distinguishable_colors(length(methods));
set(gca, 'ColorOrder', colors, 'NextPlot', 'replacechildren');
figure()
fig = plot(data(:,ordering),'LineWidth',3);
legend(methods(ordering),'Location','southeastoutside','interpreter','none')
set(gca,'XTick',1:size(data,1))
set(gca,'XTickLabel',{'superkingdom','phylum','class','order','family','genus','species'})
temp = strsplit(filename,'-');
temp = temp{end};
temp = strsplit(temp,'.');
temp = temp{1};
ylabel(temp)
set(gca, 'FontSize', 18)

%% Integrate over the metric
integrated = sum(data,1);
[~,idx] = sort(integrated,'descend');
figure()
bar(integrated(idx))
set(gca,'XTick',1:length(integrated))
set(gca, 'XTickLabel', methods(ordering))
set(gca,'XTickLabelRotation',-90);
temp = strsplit(filename,'-');
temp = temp{end};
temp = strsplit(temp,'.');
temp = temp{1};
title(temp)
set(gca, 'FontSize', 18)
ylabel('Sum over all ranks')


