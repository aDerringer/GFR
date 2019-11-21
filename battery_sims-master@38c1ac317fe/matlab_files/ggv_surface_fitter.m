clear, clc, clf

load('ggv_data.mat')

g_lat_t = G_Lat_from_GPS.Time;
g_lat_v = G_Lat_from_GPS.Value;

g_long_t = G_Long_from_GPS.Time;
g_long_v = G_Long_from_GPS.Value;

speed_t = GPS_Speed.Time;
speed_v_kph = GPS_Speed.Value;
speed_v_mps = speed_v_kph / 3.6;

percentiles = [0.057, 99.89];

[~, I] = rmoutliers(g_lat_v,'movmean', percentiles);
g_lat_v(I) = 0;

[~, I] = rmoutliers(g_long_v, 'movmean', percentiles);
g_long_v(I) = 0;

duration = min([
    g_lat_t(end)
    g_long_t(end)
    speed_t(end)
    ]);

min_num = min([
    length(g_lat_t)
    length(g_long_t)
    length(speed_t)
    ]);

t_new = linspace(0, duration, min_num);

a_lat_mpss = interp1(g_lat_t, g_lat_v, t_new).*9.81;
a_long_mpss = interp1(g_long_t, g_long_v, t_new).*9.81;
speed_mps = interp1(speed_t, speed_v_mps, t_new);

save('ggv_data_filtered.mat', 'a_lat_mpss', 'a_long_mpss', 'speed_mps')