function VecField = generateUniformField(type,numAngularVec,numTimeVec,tryGPU)
% SHADOW of WarpFactory's Analyzer/utils/generateUniformField.m (commit 03b10cb), identical except
% that the GPU flag is passed through to getEvenPointsOnSphere instead of being hard-coded to 1.
% In the original the three calls read getEvenPointsOnSphere(..., 1), so the energy-condition
% sampling demands a GPU even when getEnergyConditions is called with tryGPU = 0 and fails with
% "Error using gpuArray" on a machine without one (first CI run of shift_matrix, 26 Oct 2026).
% This folder is added to the MATLAB path after WarpFactory so this copy takes precedence.
% Candidate upstream fix: the same one-token change in the original.

if ~(strcmpi(type,"nulllike") || strcmpi(type,"timelike"))
    error('Vector field type not generated, use either: "nulllike", "timelike"')
end

if strcmpi(type,"timelike")
    % generate timelike vectors c^2t^2 > r^2,
    bb = linspace(0,1,numTimeVec);
    VecField = ones(4,numAngularVec,numTimeVec);
    for jj = 1:numTimeVec
        % build vector field in cartesian coordinates
        VecField(:,:,jj) = [ones(1,numAngularVec); getEvenPointsOnSphere(1-bb(jj),numAngularVec,tryGPU)];
        VecField(:,:,jj) = VecField(:,:,jj)./(VecField(1,:,jj).^2+VecField(2,:,jj).^2+VecField(3,:,jj).^2+VecField(4,:,jj).^2).^0.5;
    end

elseif strcmpi(type,"nulllike")
    % build vector field in cartesian coordinates
    VecField = ones(4,numAngularVec);
    VecField(2:end,:) = getEvenPointsOnSphere(1,numAngularVec,tryGPU);
    VecField = VecField./(VecField(1,:).^2+VecField(2,:).^2+VecField(3,:).^2+VecField(4,:).^2).^0.5;
end

% Declare variables to be determined in eval of E conditions
if tryGPU
    VecField = gpuArray(VecField);
end

end
