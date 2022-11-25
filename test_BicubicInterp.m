
% test bicubic interp

% Original image
Img = [];
Centroids = [];

% FM of each mesh
FMList


% resolution of mesh
res = 64;
prange = linspace(0, 1, res);

% iterate through mesh
for j  = 1 : NumMesh
    % Get 16 sample pixels
    SamplePixels = [];

    % Calculate position matrix X and Y
    yrange = linspace(-1, 2, 4)';
    xrange = linspace(-1, 2, 4);
    Y = [yrange.^3, yrange.^2, yrange, ones(4,1)];
    X = [xrange.^3; xrange.^2; xrange; ones(1,4)];

    % Iterate through pixel
    zInterp(r,c) = zeros(res, res);
    for r = 1: res
       for c = 1 : res
           % distance array PX and PY
           py = prange(r);
           px = prange(c);
           PY = [py^3, py^2, py, 1];
           PX = [py^3; px^2; px; 1];

           zInterp(r,c) = PY * inv(Y) * SamplePixels * inv(X)* PX;
       end
    end

    % applicate result of Interpolation in sub computing area
    Color_cnt = AddTexture(zInterp, FMList{j});
    
end

