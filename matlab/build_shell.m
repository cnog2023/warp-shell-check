function build_shell()
% BUILD_SHELL  Build the Fuchs et al. (2024) shell exactly as WarpFactory's own example does, and
% export what Steps 3-4 of PLAN.md need.
%
% Parameters are copied verbatim from Examples/4 Warp Shell/W1_Warp_Shell.mlx (read by unzipping the
% live script; see work/notes/04-step3-4-design.md): R1 = 10 m, R2 = 20 m, 2GM/(R2 c^2) = 1/3 so
% M = 4.49e27 kg, Rbuff = 0, sigma = 0, smoothFactor = 4000, vWarp = 0.02, grid spacing 0.2 m.
% The example runs on a "cartoon" grid: 300 x 300 cells in x and y, 5 cells in z, which gives a
% complete fourth-order stencil on the central z-plane only. We keep that configuration so the
% numbers are the authors' own; a full 3D box is a later step. GPU use is switched off.
%
% Outputs, under results/shell/:
%   params.json             every parameter used
%   profiles_<case>.csv     the 1D radial construction stored in Metric.params:
%                           r, rho, rhosmooth, P, Psmooth, M, A = g00, B = grr (SI units)
%   line_y_<case>.csv       Eulerian stress-energy along the y-axis through the centre (central z-plane)
%   line_x_<case>.csv       the same along the x-axis, the direction of motion
%   slice_<case>.mat        central-z-plane slices of the metric and of the Eulerian stress-energy (v7.3)
% for <case> = static (doWarp = 0) and warp (doWarp = 1).

outDir = fullfile(pwd, 'results', 'shell');
if ~exist(outDir, 'dir'), mkdir(outDir); end

%% parameters, verbatim from W1_Warp_Shell.mlx
spaceScale = 5;
timeScale = 1;
cartoonThickness = 5;
R1 = 10;
Rbuff = 0;
R2 = 20;
gridSize = ceil([1, 2*(R2+10)*spaceScale, 2*(R2+10)*spaceScale, cartoonThickness]);
factor = 1/3;
m = R2/(2*G)*c^2*factor;
vWarp = 0.02;
sigma = 0;
smoothFactor = 4000;
gridScaling = [1/(timeScale*spaceScale*((vWarp)*c+1)), 1/spaceScale, 1/spaceScale, 1/spaceScale];
gridScaling(1) = 1/(1000*c);
worldCenter = [(cartoonThickness+1)/2, (2*(R2+10)*spaceScale+1)/2, (2*(R2+10)*spaceScale+1)/2, (cartoonThickness+1)/2] .* gridScaling;

params = struct('R1', R1, 'R2', R2, 'Rbuff', Rbuff, 'M_kg', m, 'compactness_2GM_over_R2c2', 2*G*m/(R2*c^2), ...
    'vWarp', vWarp, 'sigma', sigma, 'smoothFactor', smoothFactor, 'gridSize', gridSize, ...
    'gridScaling', gridScaling, 'worldCenter', worldCenter, 'source', 'Examples/4 Warp Shell/W1_Warp_Shell.mlx', ...
    'matlab_version', version);
fid = fopen(fullfile(outDir, 'params.json'), 'w'); fprintf(fid, '%s\n', jsonencode(params)); fclose(fid);
fprintf('M = %.6g kg, 2GM/(R2 c^2) = %.6f, grid %s at %.3g m\n', m, 2*G*m/(R2*c^2), mat2str(gridSize), gridScaling(2));

% grid coordinates, as metricGet_WarpShellComoving defines them: x = i*gridScaling(2) - worldCenter(2)
xs = (1:gridSize(2)) * gridScaling(2) - worldCenter(2);
ys = (1:gridSize(3)) * gridScaling(3) - worldCenter(3);
zs = (1:gridSize(4)) * gridScaling(4) - worldCenter(4);
[~, i0] = min(abs(xs));          % column nearest the centre in x
[~, j0] = min(abs(ys));          % row nearest the centre in y
k0 = round((gridSize(4) + 1) / 2);   % central z-plane, the only one with a complete stencil
fprintf('centre indices (i0, j0, k0) = (%d, %d, %d) at (x, y, z) = (%.3g, %.3g, %.3g) m\n', i0, j0, k0, xs(i0), ys(j0), zs(k0));

caseNames = {'static', 'warp'};
doWarps = [0, 1];
for k = 1:2
    name = caseNames{k};
    t0 = tic;
    Metric = metricGet_WarpShellComoving(gridSize, worldCenter, m, R1, R2, Rbuff, sigma, smoothFactor, vWarp, doWarps(k), gridScaling);
    fprintf('[%s] metric built in %.1f s\n', name, toc(t0));

    % 1D construction profiles
    p = Metric.params;
    prof = [p.rVec(:), p.rho(:), p.rhosmooth(:), p.P(:), p.Psmooth(:), p.M(:), p.A(:), p.B(:)];
    writeCsv(fullfile(outDir, sprintf('profiles_%s.csv', name)), ...
        'r_m,rho_kg_m3,rhosmooth_kg_m3,P_Pa,Psmooth_Pa,M_kg,A_g00,B_grr', prof);
    fprintf('[%s] profiles: %d radial samples, dr = %.3g m\n', name, numel(p.rVec), p.rVec(2) - p.rVec(1));

    % stress-energy and its Eulerian frame
    t0 = tic;
    energy = getEnergyTensor(Metric, 0);
    eul = doFrameTransfer(Metric, energy, "Eulerian", 0);
    fprintf('[%s] stress-energy and Eulerian frame in %.1f s\n', name, toc(t0));

    % lines through the centre on the central z-plane
    header = 'coord_m,rho,p_x,p_y,p_z,P_xx,P_yy,P_zz,P_xy,P_xz,P_yz';
    comps = {[1 1], [1 2], [1 3], [1 4], [2 2], [3 3], [4 4], [2 3], [2 4], [3 4]};
    liney = zeros(gridSize(3), 1 + numel(comps));
    linex = zeros(gridSize(2), 1 + numel(comps));
    liney(:, 1) = ys(:);
    linex(:, 1) = xs(:);
    for q = 1:numel(comps)
        a = comps{q}(1); b = comps{q}(2);
        liney(:, 1 + q) = squeeze(eul.tensor{a, b}(1, i0, :, k0));
        linex(:, 1 + q) = squeeze(eul.tensor{a, b}(1, :, j0, k0));
    end
    writeCsv(fullfile(outDir, sprintf('line_y_%s.csv', name)), header, liney);
    writeCsv(fullfile(outDir, sprintf('line_x_%s.csv', name)), header, linex);

    % central-plane slices
    slice = struct();
    slice.x = xs; slice.y = ys; slice.z0 = zs(k0);
    metricComps = {[1 1], [1 2], [1 3], [1 4], [2 2], [2 3], [2 4], [3 3], [3 4], [4 4]};
    for q = 1:numel(metricComps)
        a = metricComps{q}(1); b = metricComps{q}(2);
        slice.(sprintf('g%d%d', a - 1, b - 1)) = squeeze(Metric.tensor{a, b}(1, :, :, k0));
    end
    eulNames = {'rho', 'p_x', 'p_y', 'p_z', 'P_xx', 'P_yy', 'P_zz', 'P_xy', 'P_xz', 'P_yz'};
    for q = 1:numel(comps)
        a = comps{q}(1); b = comps{q}(2);
        slice.(eulNames{q}) = squeeze(eul.tensor{a, b}(1, :, :, k0));
    end
    save(fullfile(outDir, sprintf('slice_%s.mat', name)), '-struct', 'slice', '-v7.3');

    % a few headline numbers in the log
    rhoLine = liney(:, 2);
    [rhoMax, iMax] = max(rhoLine);
    fprintf('[%s] y-line: max Eulerian energy density %.4e J/m^3 at y = %.2f m; P_yy there %.4e, P_xx there %.4e\n', ...
        name, rhoMax, ys(iMax), liney(iMax, 7), liney(iMax, 6));
    fprintf('[%s] y-line: max |P_xx| / max rho = %.4f, max |P_yy| / max rho = %.4f, min P_xx / max rho = %+.4f\n', ...
        name, max(abs(liney(:, 6))) / rhoMax, max(abs(liney(:, 7))) / rhoMax, min(liney(:, 6)) / rhoMax);
end
fprintf('done\n');
end

function writeCsv(path, header, data)
fid = fopen(path, 'w');
fprintf(fid, '%s\n', header);
fmt = [repmat('%.17g,', 1, size(data, 2) - 1), '%.17g\n'];
fprintf(fid, fmt, data');
fclose(fid);
end
