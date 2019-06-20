%% learnDecisionTree
% The algorithm for this code was outlined in the lecture notes:
%  https://eclass.srv.ualberta.ca/pluginfile.php/2897723/mod_resource/content/5/6a-DecisionTree.pdf
% on slide labeled with the number 29.
% 
% Inputs: 
%       examples            - set of examples [X1, ..., Xn, Class_label]
%                             where each row is an example and Xi (1<=i<=n)
%                             is the ith attribute (see 'id' below)
%       attributes          - attribute descriptions: a [num_attributes x 1]
%                             vector of structs with fields: 
%                                   'id'    - a unique id number
%                                   'name'  - human understandable name of attribute
%                                   'value' - possible attribute values
%
%                             Example: attribute(1) = 
%                                      id: 1
%                                      name: 'Clump Thickness'
%                                      value: [1 2 3 4 5 6 7 8 9 10]
%       default             - default predicted label
% 
% Outputs:
%       tree                - Decision Tree

function tree = learnDecisionTree(examples, attributes, default)

    %% Here's a helpful structure for creating a tree in MATLAB
    %  Each node in the tree is struct with five fields. 
    %         'attribute_id'- integer id of the attribute we split on
    %         'isleaf'      - is 'true' if the node is a leaf 
    %                         and 'false' otherwise (This should be a
	%						  boolean, not a string)
    %         'class'       - is empty if the node is not a leaf. 
    %                         If node is a leaf, class = 0 or 1
    %         'children'    - is empty if the node is a leaf. 
    %                         Otherwise, it is a cell {} where 
    %                         tree.children{i} is the subtree when the 
    %                         tree.attribute_id takes on value tree.value(i).
    %         'value'       - a vector of values that the attribute can
    %                         take. Is empty if the node is a leaf.
    %         'num_1'       - The number of training examples in class = 1
    %                         at the node.
    %         'num_0'       - The number of training examples in class = 0
    %                         at the node.
    %         'num_tot'     - The total number of training examples at the
    %                         node.
    %
    %  Example (non-leaf node):
    % 
    %     attribute_id: 1
    %           isleaf: 0
    %            class: []
    %         children: {1x10 cell}
    %            value: [1 2 3 4 5 6 7 8 9 10]
    %            num_1: 43
    %            num_0: 2
    %          num_tot: 45
    %  
    %  Example (leaf node):
    %  
    %     attribute_id: []
    %           isleaf: 1
    %            class: 0
    %         children: []
    %            value: []
    %            num_1: 43
    %            num_0: 2
    %          num_tot: 45
    
    tree = struct('attribute_id',[],...
                  'isleaf',true,...
                  'class',default,...
                  'children',[],...
                  'value',[],...
                  'num_1',-1,...
                  'num_0',-1,...
                  'num_tot',-1);             

    %% 0. If there are no examples to classify, return
    num_examples = size(examples,1);
    if num_examples == 0
        return
    end
    
    %% 1. If all examples have the same classification, create a 
    %      tree leaf node with that classification and return
    labels = examples(:, end);

    % <ENTER YOUR CODE HERE>
    if (length(unique(labels)) == 1)
        tree.isleaf = 1;
        tree.class = unique(labels);
        tree.num_0 = (tree.class==0)*num_examples;
        tree.num_1 = (tree.class==1)*num_examples;
        tree.num_tot = num_examples;
        return
    end
    
    %% 2. If attributes is empty, create a leaf node with the
    %      majority classification and return.
    
    % <ENTER YOUR CODE HERE>
    if (isempty(attributes))
        tree.isleaf = 1;
        tree.class = sum(labels)>length(examples)/2;
        tree.num_0 = length(examples)-sum(labels);
        tree.num_1 = sum(labels);
        tree.num_tot = length(examples);
        return
    end
    %% 3. Find the best attribute -- the attribute with the lowest uncertainty
    % <ENTER YOUR CODE HERE>
    best_a = zeros(size(examples(1,:))-1);
    for i=1:size(best_a,2)
        best_a(i) = uncert(i, unique(examples(:,i)), examples);
    end
    [~, best_i] = max(best_a);
    
    %% 4. Make a non-leaf tree node with root 'best'
    % 
    % <ENTER YOUR CODE HERE>
    tree.attribute_id = attributes(best_i).id;
    tree.isleaf = 0;
    tree.value = attributes(best_i).value;
    tree.num_0 = length(labels) -  sum(labels);
    tree.num_1 = sum(labels);
    tree.num_tot = length(labels);
    
    %% 5. For each value v_i that the best attribute can take, do the following:
    %     a. examples_i <-- elements of examples where the best attribute has value v_i
    %     b. subtree <-- recursive call to learnDecisionTree with inputs:
    %              examples_i
    %              all attributes but the best
    %              the majority value of the examples
    %     c. add branch to tree with label vi and subtree
    
    tree.children = cell(length(attributes(best_i).value'),1);
    for i=1:length(tree.value')
        examples_i = examples(examples(:,best_i)==tree.value(i),:);
        examples_i(:,best_i) = [];
        attributes_i = attributes;
        attributes_i(best_i) = [];       
        tree.children{i} = learnDecisionTree(examples_i, attributes_i, default);
    end
 
    return
 
end


%% You may wish to write a function that...
%  Computes the uncertainty of the i-th attribute when given:
%        i                - the id of the attribute
%        attribute_vals   - the vector of possible values that attribute
%                           can take
%        examples         - the set of examples on which you'll compute
%                           the information gain
%% 
function value = uncert(i, attribute_vals, examples)
%      <ENTER CODE HERE>
    labels = examples(:, end);
    value = 0;
    for j=1:length(attribute_vals)
       si = find(examples(:,i)==attribute_vals(j));
       value = value + entropy(sum(labels(si)), (length(labels(si))-sum(labels(si))))*(length(si)/length(labels));
    end
    value = value * (-1);

end


%% You may wish to have an entropy function that...
%  Computes entropy when given:
%        p               - the number of class = 1 examples
%        n               - the number of class = 0 examples
% [Hint: what if input is zero?]
%%
function en = entropy(p,n)
%   <ENTER CODE HERE>
    p1 = p/(p+n);
    p2 = n/(p+n);
    en = -(p1*log2(p1)+p2*log2(p2));

end
