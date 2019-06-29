from django.shortcuts import render
from stats.stats_functions import get_stats, get_time_avereges, get_most_busy_time, get_most_busy, get_longest_shower


def stats(request, entries_requested=10):
    stats = get_stats(entries_requested)

    context = {'requested_entries': entries_requested, 'times_durations': stats[0]}
    return render(request, 'stats.html', context)


def more_stats(request, entries_requested='alle'):
    stats = get_stats(entries_requested)
    

    avgs = get_time_avereges(stats[0])
    most_busy_time = get_most_busy_time(stats[0])
    most_busy = get_most_busy(stats[0])
    longest_shower = get_longest_shower(stats[0])

    context = {'requested_entries': entries_requested, 'number_of_entries': stats[1], 'avgs': avgs, 'most_busy_time': most_busy_time, 'most_busy': most_busy, 'longest_shower': longest_shower }
    return render(request, 'more_stats.html', context)
