function print_tree(tree)
    fprintf('Root\n');
    print_tree_r(tree, '');
end

function print_tree_r(tree, prefix)

    if tree.isleaf
        fprintf('Class : %d   +/- = [%d , %d] \n', tree.class, tree.num_1, tree.num_0)
    else
       prefix = [prefix , ' |'];
        for i = 1:length(tree.children)
            fprintf('%s-Attribute ID %d = %d ', prefix, tree.attribute_id, tree.value(i))
            if ~tree.children{i}.isleaf,
                fprintf('\n');
            end
            print_tree_r(tree.children{i} , prefix);
        end
    end

end