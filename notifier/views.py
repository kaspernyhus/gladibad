from django.shortcuts import render
from main.models import BrState
from django.http import HttpResponseRedirect
import os
import slack
from .slack_token import slack_token
import json


def convert_to_json(db_data):
    try:
        json_data = json.loads(db_data) #convert to json
        return json_data
    except:
        return [{"id": 0, "name": "Error", "notify": 0}]

def convert_to_str(json_data):
    str_data = json.dumps(json_data) #convert to str
    return str_data


def update_notifier(db_data, json_data):
    str_data = convert_to_str(json_data)
    db_data.notifier = str_data
    db_data.save(update_fields=['notifier'])


def connect_to_slack():
    client = slack.WebClient(token=slack_token)
    return client


def create_slack_user(request, user_name):
    db_data = BrState.objects.latest('id')
    
    slack_user_json = convert_to_json(db_data.notifier)

    number_of_users = len(slack_user_json)
    slack_user_json.append({'id': number_of_users+1, 'name': user_name, 'notify': 0})
    
    update_notifier(db_data, slack_user_json)

    #create new "channel" in slack
    """client = connect_to_slack()
    
    channel_name = f"gladibad_{user_name}"
    client.api_call("groups.create",
                 channel=channel_name)"""

    context = {'info': f'User: {user_name} created'}
    return render(request, 'info.html', context)


def notify_me(request, slack_user):
    db_data = BrState.objects.latest('id')

    if db_data.state == 1: #check if the bathroom is occupied
        
        slack_user_json = convert_to_json(db_data.notifier)

        for user in slack_user_json:
            if user['id'] == slack_user:
                user['notify'] = 1

        """if BrState.notifier > 0:
            context = {'status': 'En anden har allerede bedt om at blive notificeret'}
            return render(request, 'vip_index.html', context)"""

        update_notifier(db_data, slack_user_json)

        return HttpResponseRedirect('/')


def check_if_notify(db_data):
    slack_user_json = convert_to_json(db_data.notifier)
    
    try:
        for user in slack_user_json:
            if user['notify'] == 1:
                #try:
                send_notification(user['id'])
                #except:
                #    print('------------ Notification failed ---------------')
    except TypeError:
        pass


def reset_notifier():
    db_data = BrState.objects.latest('id')

    user_data_json = convert_to_json(db_data.notifier)

    try:
        for user in user_data_json:
            user['notify'] = 0
        
        return convert_to_str(user_data_json)
    except TypeError:
        return [{"id": 0, "name": "Error", "notify": 0}]


def send_notification(user_id):
    client = connect_to_slack()
   
    if user_id == 1:
        print('---------- Laura notified ------------')
        response = client.chat_postMessage(
            channel='#gladibad_laura',
            text="Baddet er ledigt nu!")
        assert response["ok"]
        assert response["message"]["text"] == "Baddet er ledigt nu!"
    elif user_id == 2:
        print('------------- Kasper notified --------------')
        response = client.chat_postMessage(
            channel='#gladibad_kasper',
            text="Baddet er ledigt nu!")
        assert response["ok"]
        assert response["message"]["text"] == "Baddet er ledigt nu!"
    elif user_id == 3:
        print('------------- Gabriel notified --------------')
        response = client.chat_postMessage(
            channel='#gladibad_gabriel',
            text="Baddet er ledigt nu!")
        assert response["ok"]
        assert response["message"]["text"] == "Baddet er ledigt nu!"



