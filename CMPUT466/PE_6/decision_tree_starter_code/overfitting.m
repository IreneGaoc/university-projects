function [train_acc_vector, test_acc_vector, selectedDepth] = overfitting()
    clear
    clc
    load breast_cancer_dataset
    train_acc_vector = zeros(3,1);
    test_acc_vector = zeros(3,1);

    for depth = 1:3,
        fprintf('depth: %d',depth);
        tree = learnDecisionTree_2(train_set, attribute, 0, depth);
    
        test_classification = zeros(length(test_set),1);
        train_classification = zeros(length(train_set),1);
        for i = 1:length(test_set)
            test_classification(i) = classify(tree, test_set(i,:));
        end
    
        for i = 1:length(train_set)
            train_classification(i) = classify(tree, train_set(i,:));
        end
        test_accuracy = sum(test_set(:,end) == test_classification) / length(test_set);
        train_accuracy = sum(train_set(:,end) == train_classification) / length(train_set);
        fprintf('\nTest accuracy : %f\n', test_accuracy);
        fprintf('Train accuracy : %f\n\n', train_accuracy);
        train_acc_vector(depth,1) = train_accuracy;
        test_acc_vector(depth,1) = test_accuracy;
    end
    
    [~,selectedDepth] = max(test_acc_vector);
end
