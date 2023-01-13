filename = "measurements_v2.csv";

table = readtable(filename);
mac_address = 'B8:27:EB:15:3D:99';

i = 1;

distance = [];
rcv_power = [];
est_rcv_power = [];
itu_rcv_power = [];
another_deviation = [];
itu_adapted = [];
log = [];
log_diff = [];
itu_diff= [];

rcv_power2 = [];
est_rcv_power2 = [];
itu_rcv_power2 = [];
another_deviation2 = [];
itu_adapted2 = [];
log2 = [];
log_diff2 = [];
itu_diff2= [];
distance2=[];



while string(table{i,1}) == mac_address
    distance(1,i) = table{i,6};
    rcv_power(1,i) = table{i,5};
    est_rcv_power(1,i) = table{i,11};
    itu_rcv_power(1,i)= table{i,7};
    another_deviation(1,i) = table{i,11};
%     log_atte(1,i) = table{i,12};
    itu_adapted(1,i) = table{i,12};
    log_diff(1,i) = table{i,13};
    itu_diff(1,i) = table{i,14};

    
    i = i +1;
end


for k=28:54
    distance2(1,k-27) = table{k,6};
    rcv_power2(1,k-27) = table{k,5};
    est_rcv_power2(1,k-27) = table{k,11};
    itu_rcv_power2(1,k-27)= table{k,7};
    another_deviation2(1,k-27) = table{k,14};
    log_atte2(1,k-27) = table{k,13};
%     itu_adapted2(1,i) = table{i,15};
    log_diff2(1,k-27) = table{k,13};
    itu_diff2(1,k-27) = table{k,14};

    
    k = k +1;
end

% figure(1)
% plot(distance, rcv_power, '-o')
% hold on
% set(gca, 'YDir','reverse')
% figure
% plot(distance,est_rcv_power, '-*')
% set(gca, 'YDir','reverse')
figure(1)
% plot(distance,log_diff,'-*')
plot(distance2, log_diff2, '-o','LineWidth',1,'MarkerSize',10)
hold on
% set(gca, 'YDir','reverse')
xlabel('distance (m)')
ylabel('RSS dBm')

plot(distance2,itu_diff2, '-x','LineWidth',2,'MarkerSize',10)

% figure 
% plot(distance,itu_adapted, '-<')

% plot(distance, rcv_power, '-square')
% plot(distance,log_atte,'-*')
% plot(distance, itu_diff, '-o')
% plot(distance2, rcv_power2, '-*','LineWidth',1,'MarkerSize',10)

% set(gca, 'YDir','reverse')
ax = gca;
ax.FontSize = 18;
% plot(distance, itu_diff, '-o')
% set(gca, 'YDir','reverse')
hold off

display(distance)
display(rcv_power)
display(distance2)
display(rcv_power2)
