from django.shortcuts import render
from .models import BrState
from datetime import datetime

def index(request):
    try:
        #get data(object) from db    
        db_data = BrState.objects.latest('id')
        
        # time since db timestamp
        db_timestamp = db_data.timestamp
        db_timestamp_str = str(db_timestamp)

        # make proper datetime object from db_data
        timestamp_object = datetime.strptime(db_timestamp_str, '%Y-%m-%d %H:%M:%S.%f+00:00')

        now = datetime.now()

        time_passed = now - timestamp_object
        time_passed = time_passed.total_seconds()
        time_passed_in_m = int(time_passed / 60)
    
        if db_data.state == 0:
            context = {'state': db_data.state, 'status': 'LEDIGT', 'time_passed': time_passed_in_m}
        elif db_data.state ==1:
            context = {'state': db_data.state, 'status': 'OPTAGET', 'time_passed': time_passed_in_m, 'in_que': db_data.que}
    
    except:
        context = {'state': 0, 'status': 'No Data', 'time_passed': 0}


    return render(request, 'index.html', context)


def update_db(request, state):
    
    try:
        old_state = BrState.objects.latest('id')
        in_que = old_state.que

        timestamp = datetime.now()
        new_state = BrState(state=state, timestamp=timestamp, que=in_que)
        new_state.save()
    except:
        timestamp = datetime.now()
        new_state = BrState(state=state, timestamp=timestamp, que='0')
        new_state.save()

    context = {'state': state, 'timestamp': timestamp}
    return render(request, 'updated.html', context)


def about(request):
    return render(request, 'about.html')


def update_que():
    old_state = BrState.objects.latest('id')
    in_que = old_state.que

    timestamp = old_state.timestamp
    state = old_state.state

    new_state = BrState(state=state, timestamp=timestamp, que=in_que)
    new_state.save()
    reload()