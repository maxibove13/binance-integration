import matplotlib.pyplot as plt
import csv
from datetime import datetime

# Define the csv file to write/read
csv_filename = './data/daily_alts_value.csv'


x = []
y = []
# Read daily_alts_value.csv file and assign the first column (dates) to x, and second column (values) to y, excepting the header.
with open(csv_filename, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    if header != None:
        for row in reader:
            date_time_str = row[0]
            date_time_obj = datetime.strptime(date_time_str,'%Y-%m-%d')
            x.append(date_time_obj)
            y.append(float(row[1]))

# Plot alts value historical evolution

plt.plot(x,y)
plt.xlabel('Date')
plt.ylabel('BTC')
plt.title('Altcoins evolution in BTC terms')
plt.grid()
plt.show()