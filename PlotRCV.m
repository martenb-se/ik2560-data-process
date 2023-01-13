filename = "measurements_v2.csv";

table = readtable(filename);
mac_address = 'B8:27:EB:15:3D:99';

i = 1;

distance = [];
rcv_power = [];
est_rcv_power = [];
log_est = [];
log_adapted = [];
itu_adapted = [];
log = [];
log_diff = [];
itu_diff= [];

rcv_power2 = [];
est_rcv_power2 = [];
log_est2 = [];
log_adapted2 = [];
itu_adapted2 = [];
log2 = [];
log_diff2 = [];
itu_diff2= [];
distance2=[];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
k_rcv_rssi_pi_a = [];
k_rcv_rssi_pi_b = [];
k_distance_a = [];
k_distance_b = [];
k_distance_all = [];


k_log_est = [];
k_itu_est = [];
k_log_adapted = [];
k_itu_adapted = [];
k_log_diff = [];
k_itu_diff = [];

k_log_est_a = [];
k_itu_est_a = [];
k_log_adapted_a = [];
k_itu_adapted_a = [];

k_log_diff_a = [];
k_itu_diff_a = [];
k_log_diff_b = [];
k_itu_diff_b = [];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

while string(table{i,1}) == mac_address
    distance(1,i) = table{i,6};
    rcv_power(1,i) = table{i,5};
    est_rcv_power(1,i) = table{i,11};
    log_est(1,i)= table{i,7};
    log_adapted(1,i) = table{i,11};
%     log_atte(1,i) = table{i,12};
    itu_adapted(1,i) = table{i,12};
    log_diff(1,i) = table{i,13};
    itu_diff(1,i) = table{i,14};


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
k_rcv_rssi_pi_a(1,i) = table{i, 5};
k_distance_a(1,i) = table{i,6};

k_log_est_a(1,i) = table{i,7};
k_itu_est_a(1,i) = table{i,8};
k_log_adapted_a(1,i) = table{i,11};
k_itu_adapted_a(1,i) = table{i,12};
k_log_diff_a(1,i) = table{i,13};
k_itu_diff_a(1,i) = table{i,14};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    
    i = i +1;
end


for k=28:54
    distance2(1,k-27) = table{k,6};
    rcv_power2(1,k-27) = table{k,5};
    est_rcv_power2(1,k-27) = table{k,11};
    log_est2(1,k-27)= table{k,7};
    log_adapted2(1,k-27) = table{k,11};
    log_atte2(1,k-27) = table{k,13};
%     itu_adapted2(1,i) = table{i,15};
    log_diff2(1,k-27) = table{k,13};
    itu_diff2(1,k-27) = table{k,14};


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
k_rcv_rssi_pi_b(1,k-27) = table{k, 5};    
k_distance_b(1,k-27) = table{k,6};

k_log_diff_b(1,k-27) = table{k, 13};
k_itu_diff_b(1,k-27) = table{k, 14};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

    k = k +1;
end

for j=1:54

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

k_log_est(1,j) = table{j,7};
k_itu_est(1,j) = table{j,8};
k_log_adapted(1,j) = table{j, 11};
k_itu_adapted(1,j) = table{j, 12};
k_log_diff(1,j) = table{j, 13};
k_itu_diff(1,j) = table{j, 14};
k_distance_all(1,j) = table{j, 6};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

    j = j +1;
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

hold on
% set(gca, 'YDir','reverse')
xlabel('Distance (m)')
ylabel('RSSI Difference (dBm)')

%% Figure 7 Log Normal Shadow (With Wall)
% plot(distance, log_adapted, '-o')
% plot(distance2, log_adapted2, '-*','LineWidth',1,'MarkerSize',10)


% %% Figure 9
% % plot(distance2, log_diff2, '-o','LineWidth',1,'MarkerSize',10)
% % plot(distance2,itu_diff2, '-x','LineWidth',2,'MarkerSize',10)
% 
% % figure 
% % plot(distance,itu_adapted, '-<')
% 
% % plot(distance, rcv_power, '-square')
% % plot(distance,log_atte,'-*')
% % plot(distance, itu_diff, '-o')
% % plot(distance2, rcv_power2, '-*','LineWidth',1,'MarkerSize',10)
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %% Figure 9
% hold on
% 
% % Log in Green, 'o'
% plot(k_distance_a, k_log_diff_a, '-o','LineWidth',2,'MarkerSize',10, 'Color',"#77AC30")
% 
% % ITU in Yellow, 'x'
% plot(k_distance_a, k_itu_diff_a, '-x','LineWidth',2,'MarkerSize',10,'Color',"#EDB120")
% % plot(k_distance_all, k_itu_diff, '-x','LineWidth',2,'MarkerSize',10)
% 
% 
% %% legend will not work in other places!
% %% error: Warning "Ignoring extra legend entries"
% legend('Log Normal Shadow Model', 'ITU Model', 'Location','northeast' );
% title('Comparision the Deviation of Two Different Models')
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %% Figure Chap4.2 B, model without wall, real data
% hold on
% 
% % 
% plot(k_distance_a, k_rcv_rssi_pi_a, '-v','LineWidth',2,'MarkerSize',10, 'Color',"#7E2F8E")
% 
% % 
% plot(k_distance_a, k_rcv_rssi_pi_b, '-*','LineWidth',2,'MarkerSize',10,'Color',"#A2142F")
% 
% plot(k_distance_a, k_log_est_a, '-o','LineWidth',2,'MarkerSize',10,'Color',"#77AC30")
% 
% 
% 
% %% legend will not work in other places!
% %% error: Warning "Ignoring extra legend entries"
% legend('Model B v1.2 Measured Data', 'Model B+ Measured Data', 'Log Normal Shadow Data Without Wall Attenuation','northeast' );
% title('Comparision of Log Normal Shadow Data Without Wall Attenuation and The Measured Data')
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Figure Chap4.3 B, ITU model without wall, real data
hold on

% 
plot(k_distance_a, k_rcv_rssi_pi_a, '-|','LineWidth',2,'MarkerSize',10, 'Color',"#7E2F8E")

% 
plot(k_distance_a, k_rcv_rssi_pi_b, '-*','LineWidth',2,'MarkerSize',10,'Color',"#A2142F")

plot(k_distance_a, k_itu_est_a, '-o','LineWidth',2,'MarkerSize',10,'Color',"#EDB120")



%% legend will not work in other places!
%% error: Warning "Ignoring extra legend entries"
legend('Model B v1.2 Measured Data', 'Model B+ Measured Data', 'Log Normal Shadow Data Without Wall Attenuation','northeast' );
title('Comparision of ITU Model Without Wall Attenuation and The Measured Data')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% set(gca, 'YDir','reverse')
ax = gca;
ax.FontSize = 18;
% plot(distance, itu_diff, '-o')
% set(gca, 'YDir','reverse')




display(distance)
display(rcv_power)
display(distance2)
display(rcv_power2)


hold off
