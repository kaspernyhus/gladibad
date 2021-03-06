from django.shortcuts import render
from .models import BrState
from datetime import datetime, timedelta
from vip.views import send_notification


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
        error_test = now - timedelta(days=1)

        time_passed = now - timestamp_object
        time_passed = time_passed.total_seconds()
        time_passed_in_m = int(time_passed / 60)
        
        if db_data.state == 0:
            context = {'state': db_data.state, 'status': 'LEDIGT', 'time_passed': time_passed_in_m, 'current_time': now}
        elif db_data.state == 1:
            context = {'state': db_data.state, 'status': 'OPTAGET', 'time_passed': time_passed_in_m, 'current_time': now}
        
    except:
        context = {'state': 0, 'status': 'No Data', 'time_passed': 0}
    
    if db_timestamp < error_test: # if no state update from the bathroom for more than a day
        return render(request, 'error.html', {'current_time': now})
    elif db_data.state == 1 and time_passed_in_m > 180: # if bath has been occupied for more than 3 hours
        return render(request, 'error.html', {'current_time': now})
    else:
        return render(request, 'index.html', context)


def update_db(request, state):
    old_state = BrState.objects.latest('id')
    timestamp = datetime.now()

    notify = old_state.notifier


    if state == str(old_state.state):
        status = 'Error: Repeated state'

    else:
        if notify:
            send_notification()

        new_state = BrState(state=state, timestamp=timestamp, notifier='0')
        new_state.save()
        status = 'DB updated succesfully'

    context = {'status': status, 'state': state, 'timestamp': timestamp}
    return render(request, 'updated.html', context)


def about(request):
    return render(request, 'about.html')

    

        
