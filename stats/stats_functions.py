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
        total_entries = entries_requested
    
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
    
    return [packed_times, total_entries]


def get_time_avereges(stats):
    all_days = _parse_days(stats)

    weekdays = [['Mandag'], ['Tirsdag'], ['Onsdag'], ['Torsdag'], ['Fredag'], ['Lørdag'], ['Søndag']]

    avgs = []

    colors = _get_color_times(stats)
    
    for day in all_days:
        avgs.append(_get_day_avg(day))

    packed_list = []

    for i, day in enumerate(avgs):
        packed_list.append(list(zip(day, colors[i])))

    return list(zip(weekdays, packed_list)) # [(['Mandag'], [datetime.timedelta(seconds=1028), ...]), (['Tirsdag'], [datetime.timedelta(seconds=1028), ...])]


def _get_day_avg(day):
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

    return averages 


def _get_color_times(stats):
    counts = get_avereges_counts(stats)
    total_counts = _get_total_counts(counts)
    colors = []

    for day in counts:
        color_codes = []
        for count in day[1]:
            procent = (count/total_counts)*100
            if procent > 3.5:
                color_codes.append('Tomato')
            elif 2.3 < procent <= 3.5:
                color_codes.append('Gold')
            else:
                color_codes.append('MediumSeaGreen')

        colors.append(color_codes)

    return colors


def _get_total_counts(data):
    total = 0
    for day in data:
        for count in day[1]:
            total += count

    return total

def _clean_timedata(interval):
    cl_interval = []

    for time in interval:
        if timedelta(seconds=(2600)) > time[2] > timedelta(seconds=240): # filter out timedata under 4min and over 43min
            cl_interval.append(time[2])
    
    return cl_interval


def chop_microseconds(delta):
    return delta - timedelta(microseconds=delta.microseconds)


def get_avereges_counts(stats):
    all_days = _parse_days(stats)

    weekdays = [['Mandage'], ['Tirsdage'], ['Onsdage'], ['Torsdage'], ['Fredage'], ['Lørdage'], ['Søndage']]

    counts = []

    for day in all_days:
        counts.append(_get_day_avg_counts(day))

    return list(zip(weekdays, counts))



def _get_day_avg_counts(day):
    avg_counts = []

    for time_interval in day:  # 00-03, 03-06, 06-09, 09-12, 12-15, 15-18, 18-21, 21-00
        cl_time_interval = _clean_timedata(time_interval)
        avg_counts.append(len(cl_time_interval))

    return avg_counts


def _parse_days(stats):
    monday = [[], [], [], [], [], [], [], []]
    tuesday = [[], [], [], [], [], [], [], []]
    wednesday = [[], [], [], [], [], [], [], []]
    thursday = [[], [], [], [], [], [], [], []]
    friday = [[], [], [], [], [], [], [], []]
    saturday = [[], [], [], [], [], [], [], []]
    sunday = [[], [], [], [], [], [], [], []]

    all_days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

    for data in stats:
        weekday = data[0].weekday()
        for i, day in enumerate(all_days):
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

    all_days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

    return all_days


def get_most_busy_periode(stats):
    counts = get_avereges_counts(stats)
    
    busiest_time = 0

    time_0003 = 0
    time_0306 = 0
    time_0609 = 0
    time_0912 = 0
    time_1215 = 0
    time_1518 = 0
    time_1821 = 0
    time_2124 = 0

    for weekday in counts:
        time_0003 += weekday[1][0]
        time_0306 += weekday[1][1]
        time_0609 += weekday[1][2]
        time_0912 += weekday[1][3]
        time_1215 += weekday[1][4]
        time_1518 += weekday[1][5]
        time_1821 += weekday[1][6]
        time_2124 += weekday[1][7]

        all_days = [time_0003, time_0306, time_0609, time_0912, time_1215, time_1518, time_1821, time_2124]

    for i, day in enumerate(all_days):
        if day > busiest_time:
            busiest_time = day
            time = i

    return _format_time_interval(time)


def _format_time_interval(time_interval):
        if time_interval == 0:
            return '00-03'
        elif time_interval == 1:
            return '03-06'
        elif time_interval == 2:
            return '06-09'
        elif time_interval == 3:
            return '09-12'
        elif time_interval == 4:
            return '12-15'
        elif time_interval == 5:
            return '15-18'
        elif time_interval == 6:
            return '18-21'
        elif time_interval == 7:
            return '21-00'


def get_most_busy_time(stats):
    counts = get_avereges_counts(stats)
    busiest = 0
    day_of_week = ''
    time_interval = 0

    for day in counts:
        for i, count in enumerate(day[1]):
            if count > busiest:
                busiest = count
                time_interval = i
                day_of_week = day[0][0].lower()

    return_str = str(day_of_week) + ' ' + _format_time_interval(time_interval)

    return return_str


def get_longest_shower(stats):
    longest_shower = timedelta(seconds=0)

    for data in stats:
        if data[2] > longest_shower:
            longest_shower = data[2]

    return longest_shower

