from django.shortcuts import render
from .models import BrState
from datetime import datetime
from django.http import HttpResponseRedirect    
import slack


def index(request):
    try:
        #get data(object) from db    
        db_data = BrState.objects.latest('id')
        
        # time since db timestamp
        db_timestamp = db_data.timestamp
        db_timestamp_str = str(db_timestamp)

        # make proper datetime object from db_data
        timestamp_object = datetime.strptime(db_timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        
        now = datetime.now()

        time_passed = now - timestamp_object
        time_passed = time_passed.total_seconds()
        time_passed_in_m = int(time_passed / 60)
        
        if db_data.state == 0:
            context = {'state': db_data.state, 'status': 'LEDIGT', 'time_passed': time_passed_in_m, 'current_time': now}
        elif db_data.state == 1:
            context = {'state': db_data.state, 'status': 'OPTAGET', 'time_passed': time_passed_in_m, 'current_time': now}
        
    except:
        context = {'state': 0, 'status': 'No Data', 'time_passed': 0}
    return render(request, 'index.html', context)


def update_db(request, state):
    old_state = BrState.objects.latest('id')
    timestamp = datetime.now()

    if state == str(old_state.state):
        status = 'Error: Repeated state'

    else:
        if (old_state.notifier > 0 and state == 'False'):
            send_notification(old_state.notifier)
        
        new_state = BrState(state=state, timestamp=timestamp, notifier=0)
        new_state.save()
        status = 'DB updated succesfully'

    context = {'status': status, 'state': state, 'timestamp': timestamp}
    return render(request, 'updated.html', context)


def about(request):
    return render(request, 'about.html')


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


def notify_me(request, slack_user):
    db_data = BrState.objects.latest('id')

    db_data.notifier = slack_user
    db_data.save(update_fields=['notifier'])

    return HttpResponseRedirect('/')


def vip_index(request):
    try:
        #get data(object) from db    
        db_data = BrState.objects.latest('id')
        
        # time since db timestamp
        db_timestamp = db_data.timestamp
        db_timestamp_str = str(db_timestamp)

        # make proper datetime object from db_data
        timestamp_object = datetime.strptime(db_timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        
        now = datetime.now()

        time_passed = now - timestamp_object
        time_passed = time_passed.total_seconds()
        time_passed_in_m = int(time_passed / 60)
        
        if db_data.state == 0:
            context = {'state': db_data.state, 'status': 'LEDIGT', 'time_passed': time_passed_in_m, 'current_time': now}
        elif db_data.state == 1:
            context = {'state': db_data.state, 'status': 'OPTAGET', 'time_passed': time_passed_in_m, 'current_time': now}
        
    except:
        context = {'state': 0, 'status': 'No Data', 'time_passed': 0}
    
    return render(request, 'vip_index.html', context)


def send_notification(notifier):
    print('-------- Notification send!!! -------')
    slack_token = "xoxp-621793017634-633183116789-635389614102-d7b1d2b9aff8950a6e1a4b1109afc2d2"
    client = slack.WebClient(token=slack_token)

    if notifier == 1:
        response = client.chat_postMessage(
            channel='#gladibad_laura',
            text="Baddet er ledigt nu!")
        assert response["ok"]
        assert response["message"]["text"] == "Baddet er ledigt nu!"
    elif notifier == 2:
        response = client.chat_postMessage(
            channel='#gladibad_kasper',
            text="Baddet er ledigt nu!")
        assert response["ok"]
        assert response["message"]["text"] == "Baddet er ledigt nu!"

    

        