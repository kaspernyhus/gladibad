from django.shortcuts import render
from stats.stats_functions import get_stats, get_time_avereges, get_most_busy, get_longest_shower


def stats(request, entries_requested=10):
    stats = get_stats(entries_requested)

    context = {'requested_entries': entries_requested, 'times_durations': stats}
    return render(request, 'stats.html', context)


def more_stats(request, entries_requested='alle'):
    stats = get_stats(entries_requested)

    weekdays = [['Mandag'], ['Tirsdag'], ['Onsdag'], ['Torsdag'], ['Fredag'], ['Lørdag'], ['Søndag']]
    
    avgs = get_time_avereges(stats)
    most_busy = get_most_busy(stats)
    longest_shower = get_longest_shower(stats)

    context = {'requested_entries': entries_requested, 'avgs': avgs, 'most_busy': most_busy, 'longest_shower': longest_shower }
    
    
    return render(request, 'more_stats.html', context)


        