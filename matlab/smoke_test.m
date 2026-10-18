function smoke_test()
% SMOKE_TEST  Proves WarpFactory runs on the CI runner and records what its solver returns on two
% cases with an exact answer.
%
% Case 0: Minkowski. The stress-energy must be exactly zero.
% Case A: Alcubierre at 1 m spacing in a box of half-width 10 m, v = 0.1 c, R = 5 m, sigma = 0.8 /m,
%         one time slice. T^00 is compared with Alcubierre's closed-form Eulerian energy density.
%         The same case, with the same error measure, was run through the NumPy port of this
%         solver in work/precision-probe/RESULTS.md (dx = 1 m row). Identical inputs, so the two
%         should agree to about twelve digits: that agreement is the acceptance test for the port.
%
% Requires WarpFactory on the path (see .github/workflows/matlab.yml).

outDir = fullfile(pwd, 'results', 'smoke');
if ~exist(outDir, 'dir'), mkdir(outDir); end

%% Case 0: Minkowski
gridSizeM = [1 11 11 11];
metricM = metricGet_Minkowski(gridSizeM, [1 1 1 1]);
energyM = getEnergyTensor(metricM);
maxAbsMinkowski = 0;
for mu = 1:4
    for nu = 1:4
        maxAbsMinkowski = max(maxAbsMinkowski, max(abs(energyM.tensor{mu, nu}(:))));
    end
end
fprintf('minkowski_max_abs_T = %.17g\n', maxAbsMinkowski);

%% Case A: Alcubierre, dx = 1 m
n = 21;
gridSize = [1 n n n];
worldCenter = [1 11 11 11];
gridScale = [1 1 1 1];
v = 0.1; R = 5; sigma = 0.8;
metricA = metricGet_Alcubierre(gridSize, worldCenter, v, R, sigma, gridScale);
energyA = getEnergyTensor(metricA);
T00 = squeeze(energyA.tensor{1, 1});

% exact Eulerian energy density (Alcubierre 1994), on the same grid: x = i - worldCenter
[X, Y, Z] = ndgrid((1:n) - worldCenter(2), (1:n) - worldCenter(3), (1:n) - worldCenter(4));
r = sqrt(X.^2 + Y.^2 + Z.^2);
sech2 = @(u) 1 ./ cosh(u).^2;
fprime = sigma * (sech2(sigma * (R + r)) - sech2(sigma * (R - r))) / (2 * tanh(R * sigma));
kappa = c^4 / (8 * pi * G);
T00exact = -kappa * (v^2 * (Y.^2 + Z.^2) ./ (4 * r.^2)) .* fprime.^2;
T00exact(r == 0) = 0;

% drop two cells at every edge, as the WarpFactory paper recommends
idx = 3:n-2;
num = T00(idx, idx, idx);
ex = T00exact(idx, idx, idx);
peak = max(abs(ex(:)));
err = num - ex;
maxErr = max(abs(err(:))) / peak;
rmsErr = sqrt(mean(err(:).^2)) / peak;

fprintf('alcubierre_dx1_peak_exact_J_per_m3 = %.17g\n', peak);
fprintf('alcubierre_dx1_max_err_over_peak = %.17g\n', maxErr);
fprintf('alcubierre_dx1_rms_err_over_peak = %.17g\n', rmsErr);
fprintf('numpy_port_reference: max 1.633e-01, rms 1.680e-02 (work/precision-probe/RESULTS.md)\n');
fprintf('matlab_version = %s\n', version);

save(fullfile(outDir, 'smoke_alcubierre_dx1.mat'), 'T00', 'T00exact', 'v', 'R', 'sigma', ...
     'gridScale', 'worldCenter', 'gridSize', '-v7.3');
fid = fopen(fullfile(outDir, 'smoke.json'), 'w');
fprintf(fid, ['{"minkowski_max_abs_T": %.17g, "alcubierre_dx1_peak_exact": %.17g, ' ...
              '"alcubierre_dx1_max_err_over_peak": %.17g, "alcubierre_dx1_rms_err_over_peak": %.17g, ' ...
              '"matlab_version": "%s"}\n'], maxAbsMinkowski, peak, maxErr, rmsErr, version);
fclose(fid);
end
