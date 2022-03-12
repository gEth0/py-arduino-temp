# py-arduino-temp
![Alt text](./BoardArdTemp.PNG?raw=true "Title") 
## How to use:
- From the terminal digit ``` pip install -r dependences.txt```
- Open the email.txt file and write the emails following this scheme:
0) sender@example.com 
1) password of sender@example.com
2) receiver@example.com
  (note that if you're using gmail as sender@gmail.com you have to enable 'allow app from unknown source' or google will block the login).
- Open temp_db.ino with arduino IDE software and load Dht11.zip manually from Shetch/Import Libraries and select the zip file.
- Compile the sketch and load it on your board.
- Start the Mysql database and check the connection values in main.py.
- Start main.py from terminal.

### Important:
I've used Arduino Uno with temperature-sensor Dht11 and the whole system is releated on this sensor.
You can always modify the project for your hardware and need.

#### gEth0
