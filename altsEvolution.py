import matplotlib.pyplot as plt
import csv
from datetime import datetime

# Define the csv file to write/read
csv_filename = './data/daily_alts_value.csv'

# Set fontsize of labels
label_fontsize = 14

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

alts_roi_0 = []
for i in range(len(y)):
    alts_roi_0.append(y[i]/y[0]-1)

alts_roi_1 = []
for i in range(len(y)-59):
    alts_roi_1.append(y[i]/y[58]-1)


# alts_roi = np.multiply(alts_roi_0,alts_roi1) + np.sum(alts_roi_0,alts_roi1)

# Plot alts value historical evolution

fig, ax1 = plt.subplots()

ax1.set_xlabel('Date', fontsize=label_fontsize)
ax1.set_ylabel('BTC', fontsize=label_fontsize)
ax1.plot(x, y, color='tab:blue')

plt.grid()

ax2 = ax1.twinx()
ax2.set_ylabel('extra BTC return since 08/01/21', fontsize=label_fontsize)
# ax2.plot(x, alts_roi, color='tab:blue')

fig.tight_layout()
plt.title('Altcoins evolution in BTC terms', fontsize=label_fontsize)

plt.show()