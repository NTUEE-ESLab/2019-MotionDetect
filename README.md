# MotionDectect
~~ We are using Kanban development: Situations of developing shoud be updated at the top of logs ~~

** We decide to use Iteration design pattern, when updated, a log record must be added as a reminder to each other **
## Status:
Project Stage: `Basic functions are done` 
visit https://riino.site/2019/12/27/How-to-set-up-current-work-of-MotionDetect-Dev.27th/#how-to-run to check.
**Due**: Data Storage & analysis , ML training, threhold design(uncertain)

Team number:

 -  Javier Sanguino：
     - fixed work time 
       - Monday: 12:00-18:00
       - Friday: 15:00-20:00
       - Saturday: 10:00-14:00
       - Sundays: 10:00-14:00
  
- Riino(aka Shih-Chi CHANG):
  -  fixed work time: 
     -  Thur.:  13:00--17:00 
     -  Fri.：13:00--17:00 
     -   Weekends: Anytime
  
Currently goal: 

  1. get info from the sensor
  2. send data into Pi.

## Logs:

- log 12.17 :

  Inited github `readme`.
  We are going to set a Kanban(a real board in the lab) to show the process and schedule.

- log 12.19 :
  Going to establish a simple model to transfer data from STM to Pi using `socket`,which should includes a `.py` file in each side called `link.py`
  
- log 12.20
  The remote repo of `Pi` is located on `home/git/` 
 
 - log 12.23
  Data from the STM32 is accessed continuously. Problems debugguging, ready to merge with sockets for communication with RaspPi
  
 - log 12.27 （mid-term report)
  All basic functions are Successfully done:  WIFI,socket,censor of STM32, WIFI,socket on Python.
  I use my laptop to edit/run python. Those codes should be easy to just copy and run in Pi.
