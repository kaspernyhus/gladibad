from django.shortcuts import render
from stats.stats_functions import get_stats, get_time_avereges, get_most_busy_periode, get_most_busy_time, get_longest_shower


def stats(request, entries_requested=10):
    stats = get_stats(entries_requested)

    context = {'requested_entries': entries_requested, 'times_durations': stats[0]}
    return render(request, 'stats.html', context)


def more_stats(request, entries_requested='alle'):
    stats = get_stats(entries_requested)
    
    avgs = get_time_avereges(stats[0])
    most_busy_periode = get_most_busy_periode(stats[0])
    most_busy_time = get_most_busy_time(stats[0])
    colors = ['red', 'green']

    context = {'requested_entries': entries_requested, 'number_of_entries': stats[1], 'avgs': avgs, 'most_busy_periode': most_busy_periode, 'most_busy_time': most_busy_time, 'colors': colors }
    return render(request, 'more_stats.html', context)
