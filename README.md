# MotionDectect
~~ We are using Kanban development: Situations of developing shoud be updated at the top of logs ~~

** We decide to use Iteration design pattern, when updated, a log record must be added as a reminder to each other **
## Status:
Project Stage: `Basic functions are done` 
visit https://riino.site/2019/12/27/How-to-set-up-current-work-of-MotionDetect-Dev.27th/#how-to-run to check.
**Final Report is delay. New DDL : 1.14 16:00

Team number:

 -  Javier Sanguino：
     - fixed work time 
       - Monday: 12:00-18:00
       - Friday: 15:00-20:00
       - Saturday: 10:00-14:00
       - Sundays: 10:00-14:00
     - final day for flight:
       - 10th, Jan.  2020.
  
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
 - log 1.9 
  We made some extra format adjustment to keep the length of data that everytime STM32 sends fixed.
  On 1.9, we have `store_recieve.py` to pick a fixed length of data stream from STM32,and save the data as a `.csv` file with a input lable `PASS : 0, SHOOT: 1` for training.
  Also, the installation of pytorch in Pi is running. According to doc it will take 3 hours.
  - log 1.10 (final report in schedule)
  //TODO
