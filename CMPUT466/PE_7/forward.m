function [alpha, P] = forward(O, phi, A, B)
% Given size-T observation, O, and HMM parameters corresponding to k 
% states, forward.m computes and returns the forward matrix, alpha, of 
% size T*k, where alpha(t,i) = Prob(O_{1},O_{2},....O_{t}, D_t=i) and P, 
% of size 1*T, where P(t)=Prob(O_{1},O_{2},....O_{t})
%
% Input:
%   O: sequence of Observations (1*T)
%   phi: initial state distribution of HMM (1*k)
%   A: HMM transition matrix (k*k)
%   B: HMM emission matrix (m*k)
%
% Returns:
%   alpha: forward matrix (T*k)
%   P: probability of the observation sequence (T*1)
%
%   See Eqn 18 in Rabiner 1989 for details
T = length(O); % size of observation sequence
m= size(B,1);  % number of possible observed values
k = size(A,1);  % number of possible states
alpha = zeros(T, k);
P = zeros(T,1);
%Your code goes here
alpha = phi .* B(O(1),:); 
for i=2:T
    alpha(i,:) = (alpha(i-1,:) * A) .* B(O(i),:);
end
P = sum(alpha,2);
end
