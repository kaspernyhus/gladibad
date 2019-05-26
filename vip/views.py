from django.shortcuts import render
from datetime import datetime
from main.models import BrState


def avg_ocupancy(time_of_day):
    #return datetime minutes
    pass


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
        

        #avg_ocupancy(now)
        avg_ocupancy = 12

        if db_data.state == 0:
            context = {'state': db_data.state, 'status': 'LEDIGT', 'time_passed': time_passed_in_m, 'current_time': now}
        elif db_data.state == 1:
            context = {'state': db_data.state, 'status': 'OPTAGET', 'time_passed': time_passed_in_m, 'current_time': now, 'avg_ocu': avg_ocupancy}
        
    except:
        context = {'state': 0, 'status': 'No Data', 'time_passed': 0}
    
    return render(request, 'vip_index.html', context)