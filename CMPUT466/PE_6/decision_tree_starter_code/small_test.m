clear
clc
% load breast_cancer_dataset
load breast_cancer_dataset
tree = learnDecisionTree(train_set, attribute, 0);
%print_tree(tree)
corr = 0;
for i = 1:length(train_set)
    classification1 = classify(tree, train_set(i,:));
    if classification1 == train_set(i,end)
        corr = corr + 1;
    end
end
disp(corr);
cor = 0;

for i = 1:length(test_set)
    classification2 = classify(tree, test_set(i,:));
    if classification2 == test_set(i,end)
        cor = cor + 1;
    end
end
disp(cor);
%% If your learnDecisionTree() and classify() functions work,
%  you should see the following output:
%
% Root
%  |-Attribute ID 1 = 0 
%  | |-Attribute ID 2 = 0 Class : 1   +/- = [127 , 11] 
%  | |-Attribute ID 2 = 1 Class : 0   +/- = [43 , 238] 
%  |-Attribute ID 1 = 1 
%  | |-Attribute ID 2 = 0 Class : 0   +/- = [16 , 123] 
%  | |-Attribute ID 2 = 1 Class : 1   +/- = [163 , 29] 
% 
% classification =
% 
%      0
