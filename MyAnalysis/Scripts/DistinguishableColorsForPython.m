for N=1:36
    colors = distinguishable_colors(N);
    fprintf('[')
    for i=1:size(colors,1)
        fprintf('[%f,%f,%f]',colors(i,1), colors(i,2), colors(i,3))
        if i~=N
            fprintf(',')
        end
    end
    fprintf(']\n')
end
