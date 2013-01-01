import numpy as np
from pandas import *
import matplotlib.pyplot as plt
from pylab import figure, show
from datetime import timedelta

df = read_csv('training.csv', sep = ' , ', 
              names=[ 'date', 'activity', 'distance', 'duration'])
df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))

def timetominutes(time):
    a = map(float, time.split(":"))
    return (a[0] + a[1]/60)

df['duration'] = df['duration'].apply(timetominutes)

mara_dates = map(lambda x: datetime.strptime(x, '%d/%m/%Y'), 
                 [ '17/04/2011', '17/09/2011', '01/07/2012' ])

mara_dfs = []
for mara_date in mara_dates:
    twenty_weeks_before = mara_date - timedelta(weeks=20)
    mara_dfs.append(df[(df['date'] < mara_date) & 
                       (df['date'] > twenty_weeks_before) & 
                       (df['activity'] == 'run')])

for idx, mara_df in enumerate(mara_dfs):
    def weeks_difference(date1, date2): 
        return abs((date1-date2).days)/7 
    mara_df['weeks_before'] = \
        mara_df['date'].apply(lambda x: weeks_difference(x, mara_dates[idx]))

fig = plt.figure()
plt.title('Running hours vs. weeks until marathon')

colours = ['red', 'green', 'blue']

rects = []
for idx, mara_df in enumerate(mara_dfs):
    grouped = mara_df.groupby('weeks_before').sum()
    ax = fig.add_subplot(111)
    rects.append(ax.bar(19-grouped.index+idx*0.25, 
                        grouped['duration'].values, 
                        0.25 , color=colours[idx]))

ticks = np.arange(19, -1, -1)
ax.set_xticks(19-ticks+0.375)
ax.set_xticklabels(ticks)
ax.legend(rects, map(lambda x: datetime.strftime(x, '%d/%m/%Y'), 
                     mara_dates))
ax.set_xlabel("weeks to go")
ax.set_ylabel("running hours")

plt.show()
