function [qstar] = viterbi(O, phi, A, B)
% Given size T observation, O, and HMM parameters corresponding to k states,
% viterbi.m computes and returns qstar vector of size 1*T of most likely
% state interpretation for a given O
%
% Input:
%   O: sequence of Observations (1*T)
%   phi: initial state distribution of HMM (1*k)
%   A: HMM transition matrix (k*k)
%   B: HMM emission matrix (m*k)
%
% Returns:
%   qstar: most likely state interpretation for the given O (1*T)
%
%   See Eqn 32a-35 in Rabiner 1989 for details
T = length(O); % size of observation sequence
m = size(B,1);  % number of possible observed values
k = size(A,1);  % number of possible states
qstar = zeros(1,T);

%Your code goes here
d(1,:) = phi.*B(O(1),:);
X(1,:) = [0,0];
for i=2:T
    
    [max_value,X(i,:)] = max(transpose(d(i-1,:)) .* A);
    d(i,:) =max_value .* B(O(i),:);
      
end
[~, qstar(T)] =  max(d(T,:));
for i =T:-1:2
    qstar(i-1) =  X(i, qstar(:,i));
end
end
