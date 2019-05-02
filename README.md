# gladibad.pythonanywhere.com

This project persists of two parts; an [Arduino](https://www.arduino.cc/) senory module and a [Django](https://www.djangoproject.com/) web page displaying results.

The overall goal is to couple these to parts to deliver sensory results on a webpage. The particular application is light sensoring to determine whether a shared bathroom is available or not.

## Arduino sensory module

The part only consists of one file, which is located in the [Arduino](Arduino/) folder. All this file does is run a loop that checks if the sensored light is above or below a certain threshold and sends an update if the state changes.

## Django web page

This part of the project exposes an API endpoint, [`GET changestate/<state>/`](main/urls.py#7), to update the light state in the database and a few html pages to display the information.
 