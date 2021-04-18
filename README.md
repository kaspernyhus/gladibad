# gladibad.pythonanywhere.com

This project persists of two parts; an [Arduino](https://www.arduino.cc/) senory module and a [Django](https://www.djangoproject.com/) web page displaying results.

The overall goal is to couple these to parts to deliver sensory results on a webpage. The particular application is light sensoring to determine whether a shared bathroom is available or not.

## Arduino sensory module
The part only consists of one file, which is located in the [Arduino](Arduino/) folder. All this file does is run a loop that checks if the sensored light is above or below a certain threshold and sends an update if the state changes.

## Django web page
This part of the project exposes an API endpoint, [`GET changestate/<state>/`](main/urls.py#7), to update the light state in the database and a few html pages to display the information.


## Project pictures
![2019-05-01 14 56 05](https://user-images.githubusercontent.com/46648238/115159831-54e81800-a095-11eb-82d9-edb67eafac92.jpg)
![2019-05-01 21 50 06](https://user-images.githubusercontent.com/46648238/115159833-56194500-a095-11eb-9d60-8c5859ed8264.jpg)
<img width="300" alt="ledigt" src="https://user-images.githubusercontent.com/46648238/115159834-574a7200-a095-11eb-835e-dbf6ceb9905b.png">
<img width="461" alt="optaget" src="https://user-images.githubusercontent.com/46648238/115159835-57e30880-a095-11eb-8098-db87916d70f0.png">