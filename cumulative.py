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

xss = []
yss = []
for idx, mara_df in enumerate(mara_dfs):
    def days_difference(date1, date2): 
        return (date1-date2).days
    xss.append(
        mara_df['date'].apply(lambda x: days_difference(x, mara_dates[idx])))
    yss.append(np.cumsum(mara_df['duration']))


fig = plt.figure()
plt.title('Cumulative hours run before marathon')

colours = ['red', 'green', 'blue']

ticks = np.arange(140, -1, -7)

lines=[]
for idx, xs in enumerate(xss):
    plt.plot(xs,yss[idx], label=datetime.strftime(mara_dates[idx], '%d/%m/%Y'))

ax = plt.axes()
ax.set_xticklabels(ticks)
ax.legend()
ax.set_xlabel("days to go")
ax.set_ylabel("running hours")

plt.show()
