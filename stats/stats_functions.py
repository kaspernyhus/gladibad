from main.models import BrState
from datetime import datetime, timedelta


def get_stats(entries_requested):
    
    if entries_requested == 'alle':
        total_data = db_data = BrState.objects.all().order_by('-id')
        td_number = len(total_data) // 2
        total_entries = td_number - 103
        number_of_entries_requested = total_entries * 2
    else:
        number_of_entries_requested = entries_requested * 2
    
    db_data = BrState.objects.all().order_by('-id')[0:number_of_entries_requested]
    
    on_timestamps = []
    off_timestamps = []
    
    for data in db_data:
        if data.state == 1:
            on_timestamps.append(data.timestamp)
        elif data.state == 0:
            off_timestamps.append(data.timestamp)
    
    durations = []
    
    if on_timestamps[0] < off_timestamps[0]:
        for i, on_time in enumerate(on_timestamps):
            on_timestamp_object = datetime.strptime(str(on_time), '%Y-%m-%d %H:%M:%S.%f')
            off_timestamp_object = datetime.strptime(str(off_timestamps[i]), '%Y-%m-%d %H:%M:%S.%f')

            duration = off_timestamp_object.replace(microsecond=0) - on_timestamp_object.replace(microsecond=0)

            durations.append(duration)

    else:
        on_timestamps = on_timestamps[1:]
        for i, on_time in enumerate(on_timestamps):
            on_timestamp_object = datetime.strptime(str(on_time), '%Y-%m-%d %H:%M:%S.%f')
            off_timestamp_object = datetime.strptime(str(off_timestamps[i]), '%Y-%m-%d %H:%M:%S.%f')

            duration = off_timestamp_object.replace(microsecond=0) - on_timestamp_object.replace(microsecond=0)

            durations.append(duration)

    packed_times = list(zip(on_timestamps, off_timestamps, durations))
    
    return packed_times
 

def chop_microseconds(delta):
    return delta - timedelta(microseconds=delta.microseconds)


def _clean_timedata(interval):
    cl_interval = []

    for time in interval:
        if time[2] > timedelta(seconds=(240)): # filter out times under 4 minutes
            cl_interval.append(time[2])
    
    return cl_interval


def _get_avg(day):
    averages = []

    for time_interval in day:  # 00-03, 03-06, 06-09, 09-12, 12-15, 15-18, 18-21, 21-00
        
        total = timedelta(seconds=0)
        
        cl_time_interval = _clean_timedata(time_interval)

        for time in cl_time_interval:
            total += time

        try:
            avg = total / len(cl_time_interval)
            avg = chop_microseconds(avg)
        except ZeroDivisionError:
            avg = 'N/A'

        averages.append(avg)
        averages.append(len(cl_time_interval))

    return averages 


def _parse_days(stats):
    _monday = [[], [], [], [], [], [], [], []]
    _tuesday = [[], [], [], [], [], [], [], []]
    _wednesday = [[], [], [], [], [], [], [], []]
    _thursday = [[], [], [], [], [], [], [], []]
    _friday = [[], [], [], [], [], [], [], []]
    _saturday = [[], [], [], [], [], [], [], []]
    _sunday = [[], [], [], [], [], [], [], []]

    _all_days = [_monday, _tuesday, _wednesday, _thursday, _friday, _saturday, _sunday]

    for data in stats:
        weekday = data[0].weekday()

        for i, day in enumerate(_all_days):

            if weekday == i:
                if 0 <= data[0].hour <= 3:
                    day[0].append(data)
                elif 3 < data[0].hour <= 6:
                    day[1].append(data)
                elif 6 < data[0].hour <= 9:
                    day[2].append(data)
                elif 9 < data[0].hour <= 12:
                    day[3].append(data)
                elif 12 < data[0].hour <= 15:
                    day[4].append(data)
                elif 15 < data[0].hour <= 18:
                    day[5].append(data)
                elif 18 < data[0].hour <= 21:
                    day[6].append(data)
                elif 21 < data[0].hour <= 24:
                    day[7].append(data)

    _all_days = [_monday, _tuesday, _wednesday, _thursday, _friday, _saturday, _sunday]

    return _all_days


def get_time_avereges(stats):
    all_days = _parse_days(stats)

    weekdays = [['Mandag'], ['Tirsdag'], ['Onsdag'], ['Torsdag'], ['Fredag'], ['Lørdag'], ['Søndag']]

    avgs = []

    for day in all_days:
        avgs.append(_get_avg(day))

    return list(zip(weekdays, avgs))


def get_most_busy(stats):
    avgs = get_time_avereges(stats)
    busiest = 0
    day_of_week = ''
    time_interval = 0

    for weekday in avgs:
        for day in weekday:
            for i, time in enumerate(day):
                if isinstance(time, int):
                    if time > busiest:
                        busiest = time
                        day_of_week = weekday[0]
                        time_interval = i


    def format_time_interval(time_interval):
        if time_interval == 1:
            return '00-03'
        elif time_interval == 3:
            return '03-06'
        elif time_interval == 5:
            return '06-09'
        elif time_interval == 7:
            return '09-12'
        elif time_interval == 9:
            return '12-15'
        elif time_interval == 11:
            return '15-18'
        elif time_interval == 13:
            return '18-21'
        elif time_interval == 15:
            return '21-00'

    return_str = str(day_of_week[0]) + ' ' + format_time_interval(time_interval)

    return return_str


def get_longest_shower(stats):
    longest_shower = timedelta(seconds=0)

    for data in stats:
        if data[2] > longest_shower:
            longest_shower = data[2]

    return longest_shower