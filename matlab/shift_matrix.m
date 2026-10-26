function shift_matrix()
% SHIFT_MATRIX  How much shift the shell can carry, against its compactness (PLAN.md Part 1A).
%
% For each compactness the static shell and the unit-shift shell are built once. The construction
% sets g01 = -beta * S(r) on a static g01 of zero (metricGet_WarpShellComoving.m, last lines), so the
% warp metric for any beta is the static metric with g01 = beta * g01(unit shift). That is checked
% numerically against a direct build at beta = 0.02 for the first compactness. For each beta the
% script computes the stress-energy, its Eulerian frame, and WarpFactory's own sampled energy
% conditions (100 directions x 10 speeds, the paper's setting) on the three central z-planes, which
% is where the cartoon grid's stencil is complete.
%
% Exports, under results/matrix/:
%   summary.csv                 one row per (compactness, beta): plane minima of the four conditions,
%                               Eulerian energy density and momentum extremes, timings
%   profiles_f<a>.csv           the 1D construction for compactness index a (independent of beta)
%   slice_f<a>_b<b>.mat (v7)    central-plane slices: Eulerian stress-energy (10 components), the four
%                               energy-condition maps, six metric components, coordinates
% Edge cells are kept in the files and dropped (two per side) in the summary.

outDir = fullfile(pwd, 'results', 'matrix');
if ~exist(outDir, 'dir'), mkdir(outDir); end

%% authors' configuration (W1_Warp_Shell.mlx); only the mass is varied
spaceScale = 5; timeScale = 1; cartoonThickness = 5;
R1 = 10; Rbuff = 0; R2 = 20;
gridSize = ceil([1, 2*(R2+10)*spaceScale, 2*(R2+10)*spaceScale, cartoonThickness]);
sigma = 0; smoothFactor = 4000;
vRef = 0.02;
gridScaling = [1/(timeScale*spaceScale*((vRef)*c+1)), 1/spaceScale, 1/spaceScale, 1/spaceScale];
gridScaling(1) = 1/(1000*c);
worldCenter = [(cartoonThickness+1)/2, (2*(R2+10)*spaceScale+1)/2, (2*(R2+10)*spaceScale+1)/2, (cartoonThickness+1)/2] .* gridScaling;
xs = (1:gridSize(2)) * gridScaling(2) - worldCenter(2);
ys = (1:gridSize(3)) * gridScaling(3) - worldCenter(3);
k0 = round((gridSize(4) + 1) / 2);
kk = (k0-1):(k0+1);                 % three central planes for the sampled conditions
inner = 3:gridSize(2)-2;            % drop two edge cells per side in the summary

factors = [1/3, 1/10, 1/30, 1/100];
% First run (26 Oct 2026, run 40406621961): betas = [0 0.01 0.02 0.04 0.08 0.16] at every compactness.
% It showed the first failing shift scaling with the compactness C (momentum density grows as
% beta / C relative to the energy density), so this refined run samples beta in units of C.
betaOverC = [0, 0.02, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12, 0.15];
numAng = 100; numTime = 10;
names = {'rho', 'p_x', 'p_y', 'p_z', 'P_xx', 'P_yy', 'P_zz', 'P_xy', 'P_xz', 'P_yz'};
comps = {[1 1], [1 2], [1 3], [1 4], [2 2], [3 3], [4 4], [2 3], [2 4], [3 4]};
header = 'factor,compactness,M_kg,beta,rho0_J_m3,minNull,minWeak,minStrong,minDominant,minRhoEul,maxAbsMomentum,tBuild_s,tT_s,tEC_s';
rows = [];

fprintf('grid %s at %.3g m; betas %s; sampling %d x %d\n', mat2str(gridSize), gridScaling(2), mat2str(betas), numAng, numTime);
for a = 1:numel(factors)
    f = factors(a);
    m = R2 / (2*G) * c^2 * f;
    t0 = tic;
    M0 = metricGet_WarpShellComoving(gridSize, worldCenter, m, R1, R2, Rbuff, sigma, smoothFactor, 0, 0, gridScaling);
    M1 = metricGet_WarpShellComoving(gridSize, worldCenter, m, R1, R2, Rbuff, sigma, smoothFactor, 1, 1, gridScaling);
    tBuild = toc(t0);
    S01 = M1.tensor{1, 2};          % g01 of the unit-shift shell, = -S(r) on the grid
    fprintf('factor %.4g: M = %.4e kg, compactness %.4f, two builds in %.1f s\n', f, m, 2*G*m/(R2*c^2), tBuild);
    if a == 1
        Mchk = metricGet_WarpShellComoving(gridSize, worldCenter, m, R1, R2, Rbuff, sigma, smoothFactor, vRef, 1, gridScaling);
        d = max(abs(Mchk.tensor{1, 2}(:) - vRef * S01(:)));
        fprintf('linearity check at beta = %.3g: max |g01(direct) - beta*g01(unit)| = %.3e, max |g01| = %.3e\n', ...
            vRef, d, max(abs(Mchk.tensor{1, 2}(:))));
    end
    p = M0.params;
    prof = [p.rVec(:), p.rho(:), p.rhosmooth(:), p.P(:), p.Psmooth(:), p.M(:), p.A(:), p.B(:)];
    writeCsv(fullfile(outDir, sprintf('profiles_f%d.csv', a)), 'r_m,rho_kg_m3,rhosmooth_kg_m3,P_Pa,Psmooth_Pa,M_kg,A_g00,B_grr', prof);

    for b = 1:numel(betas)
        beta = betas(b);
        Metric = M0;
        Metric.tensor{1, 2} = beta * S01;
        Metric.tensor{2, 1} = Metric.tensor{1, 2};
        t1 = tic;
        energy = getEnergyTensor(Metric, 0);
        eul = doFrameTransfer(Metric, energy, "Eulerian", 0);
        tT = toc(t1);

        Ms = sliceStruct(Metric, kk);
        Es = sliceStruct(energy, kk);
        t2 = tic;
        nullMap = getEnergyConditions(Es, Ms, "Null", numAng, numTime, 0, 0);
        weakMap = getEnergyConditions(Es, Ms, "Weak", numAng, numTime, 0, 0);
        strongMap = getEnergyConditions(Es, Ms, "Strong", numAng, numTime, 0, 0);
        domMap = getEnergyConditions(Es, Ms, "Dominant", numAng, numTime, 0, 0);
        tEC = toc(t2);

        nullC = squeeze(nullMap(1, :, :, 2));
        weakC = squeeze(weakMap(1, :, :, 2));
        strongC = squeeze(strongMap(1, :, :, 2));
        domC = squeeze(domMap(1, :, :, 2));
        rhoC = squeeze(eul.tensor{1, 1}(1, :, :, k0));
        momC = sqrt(squeeze(eul.tensor{1, 2}(1, :, :, k0)).^2 + squeeze(eul.tensor{1, 3}(1, :, :, k0)).^2 + squeeze(eul.tensor{1, 4}(1, :, :, k0)).^2);
        rho0 = max(max(rhoC(inner, inner)));
        row = [f, 2*G*m/(R2*c^2), m, beta, rho0, ...
               min(min(nullC(inner, inner))), min(min(weakC(inner, inner))), min(min(strongC(inner, inner))), min(min(domC(inner, inner))), ...
               min(min(rhoC(inner, inner))), max(max(momC(inner, inner))), tBuild, tT, tEC];
        rows(end+1, :) = row; %#ok<AGROW>
        fprintf('  beta %.3f: rho0 %.3e; min/rho0: null %+.3e weak %+.3e strong %+.3e dominant %+.3e; max|p|/rho0 %.3f; T %.1f s, EC %.1f s\n', ...
            beta, rho0, row(6)/rho0, row(7)/rho0, row(8)/rho0, row(9)/rho0, row(11)/rho0, tT, tEC);

        slice = struct('x', xs, 'y', ys, 'factor', f, 'M_kg', m, 'beta', beta, 'rho0', rho0);
        for q = 1:numel(names)
            slice.(names{q}) = squeeze(eul.tensor{comps{q}(1), comps{q}(2)}(1, :, :, k0));
        end
        slice.null = nullC; slice.weak = weakC; slice.strong = strongC; slice.dominant = domC;
        slice.g00 = squeeze(Metric.tensor{1, 1}(1, :, :, k0));
        slice.g01 = squeeze(Metric.tensor{1, 2}(1, :, :, k0));
        slice.g11 = squeeze(Metric.tensor{2, 2}(1, :, :, k0));
        slice.g12 = squeeze(Metric.tensor{2, 3}(1, :, :, k0));
        slice.g22 = squeeze(Metric.tensor{3, 3}(1, :, :, k0));
        slice.g33 = squeeze(Metric.tensor{4, 4}(1, :, :, k0));
        save(fullfile(outDir, sprintf('slice_f%d_b%d.mat', a, b)), '-struct', 'slice', '-v7');
    end
    writeCsv(fullfile(outDir, 'summary.csv'), header, rows);   % rewritten after every compactness
end
fprintf('done\n');
end

function s = sliceStruct(s, kk)
for a = 1:4
    for b = 1:4
        s.tensor{a, b} = s.tensor{a, b}(:, :, :, kk);
    end
end
end

function writeCsv(path, header, data)
fid = fopen(path, 'w');
fprintf(fid, '%s\n', header);
fmt = [repmat('%.17g,', 1, size(data, 2) - 1), '%.17g\n'];
fprintf(fid, fmt, data');
fclose(fid);
end
