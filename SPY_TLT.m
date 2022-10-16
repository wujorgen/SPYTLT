%use Import Data in Home tab
%change date column from datetime to text
%will read in table format
%replace table '/' with '-' to convert to date time 
%    allows us to extract month and day


SPY_data = [];
for i = [1:1:height(SPYTLTTestingSPYRaw)]
    date_temp = strrep(table2array( SPYTLTTestingSPYRaw(i,1) ) , "/", "-");
    date_temp = datetime(date_temp,'InputFormat','MM-dd-yyyy HH:mm:ss');
    month_temp = month(date_temp);
    day_temp = day(date_temp);
    year_temp = year(date_temp);
    price_temp = table2array( SPYTLTTestingSPYRaw(i,2) );
    SPY_data = [SPY_data; [year_temp, month_temp, day_temp, price_temp, 0, 0]];
end

TLT_data = [];
for i = [1:1:height(SPYTLTTestingTLTRaw)]
    date_temp = strrep(table2array( SPYTLTTestingTLTRaw(i,1) ) , "/", "-");
    date_temp = datetime(date_temp,'InputFormat','MM-dd-yyyy HH:mm:ss');
    month_temp = month(date_temp);
    day_temp = day(date_temp);
    year_temp = year(date_temp);
    price_temp = table2array( SPYTLTTestingTLTRaw(i,2) );
    TLT_data = [TLT_data; [year_temp, month_temp, day_temp, price_temp, 0, 0]];
end

n = 2; %find 'n' month return
m=0;
newMonth = False

for i = [1;1;height(SPYTLTTestingSPYRaw)]
    
end

for i = [1;1;height(SPYTLTTestingTLTRaw)]
    
end