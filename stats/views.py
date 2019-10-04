from django.shortcuts import render
from stats.stats_functions import get_stats, get_time_avereges, get_most_busy_periode, get_most_busy_time, get_longest_shower, _get_color_times
from datetime import datetime, timedelta


def stats(request, entries_requested=10):
    stats = get_stats(entries_requested)

    context = {'requested_entries': entries_requested, 'times_durations': stats[0]}
    return render(request, 'stats.html', context)


def averages(request, entries_requested='alle'):
    stats = get_stats(entries_requested)
    
    avgs = get_time_avereges(stats[0])
    most_busy_periode = get_most_busy_periode(stats[0])
    most_busy_time = get_most_busy_time(stats[0])
    colors = _get_color_times(stats[0])

    context = {'requested_entries': entries_requested, 'number_of_entries': stats[1], 'avgs': avgs, 'most_busy_periode': most_busy_periode, 'most_busy_time': most_busy_time, 'colors': colors }
    return render(request, 'averages.html', context)


def latest(request):
    stats = get_stats(1)
    now = datetime.now()
    interval = (now - timedelta(seconds=(900)))

    try:
        if stats[0][0][1] > interval:
            show_flag = True

        else:
            show_flag = False
    except:
        show_flag = 'Optaget'


    context = {'time_duration': stats[0], 'current_time': now, 'show': show_flag}
    return render(request, 'seneste.html', context)