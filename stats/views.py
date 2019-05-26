from django.shortcuts import render
from main.models import BrState
from datetime import datetime


def stats(request, entries_requested=10):
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

    context = {'requested_entries': entries_requested, 'times_durations': packed_times}
    return render(request, 'stats.html', context)