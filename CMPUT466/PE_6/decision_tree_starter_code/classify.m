function [classification] = classify(tree, instance)
% classify   Classifies a single data instance by given tree
% Inputs:
%       tree            - the decision tree
%       instance        - the one example you wish to classify
% Outputs:
%       classification     - class assigned by tree, 0 or 1

% Case 1: You are at a leaf. 
if tree.isleaf
%   <ENTER YOUR CODE HERE>
    classification = tree.class;

% Case 2: You aren't at a leaf.

else 
%   <ENTER YOUR CODE HERE> 
    if (instance(tree.attribute_id))
        child = tree.children{1};
        classification = classify(child,instance);
    else
        child = tree.children{2};
        classification = classify(child,instance);
    end

end
 
end