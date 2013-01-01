import fitparse
import sys
import time
from datetime import datetime, date

def parse(filename):
    activity = fitparse.Activity(filename)
    activity.parse()

    data = list(activity.get_records_by_type('session'))[0]
    duration = data.get_data('total_timer_time') / 60
    distance = data.get_data('total_distance') / 1000
    sport = data.get_data('sport')
    activity_date = data.get_data('start_time')

    print "{}, {}, {:.3f}, {:.3f}".format(activity_date.strftime("%d/%m/%Y"), sport, distance, duration)


if __name__ == '__main__':
    args = sys.argv[1:] or [ '/Users/will/Library/Application Support/Garmin/Devices/3817962169/Activities/20121231-164229-1-1018-ANTFS-4-0.FIT' ]
    for arg in args:
        parse(arg)
