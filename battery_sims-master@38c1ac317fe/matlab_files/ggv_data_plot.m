clear, clc, clf

load('ggv_data_filtered.mat')

plot3(a_long_mpss, a_lat_mpss, speed_mps)
xlabel('Longitudinal Acceleration [m/s^2]')
ylabel('Lateral Acceleration [m/s^2]')
zlabel('Speed [m/s]')
axis equal

c_1 = 1618;
c_2 = 2.777;
c_3 = 300.0;

m = 165.0;

v = linspace(0, 25, 1000);

f_down = @(v) c_1 + c_2*(v.^2);

f_lat = @(v) c_1 + c_2*c_3*tanh(v.^2 ./c_3);

plot(f_down(v)/m, v); hold on;

plot(f_lat(v)/m, v)

xlabel('Accleration [m/s^2]')
ylabel('Velocity [m/s]')

legend('Downforce', 'Lateral Acceration')