# StrangerDanger

This program was an attempt to turn my computer into a security device. The original idea was to utilize the computers built in bluetooth capabilities to keep track of 'safe' devices and warn the user when new devices appear in range. Unfortunately in its current state this does not work due the adoption of [resolvable random private addresses](https://www.novelbits.io/bluetooth-address-privacy-ble/), which make it virtually impossible to track individual devices without an IRK. 

The program runs by calling the application.py file, which will generate or open an existing sqlite3 database and also creates a super basic flask webpage that acts as the program interface. The interface has three buttons:\
        1. Safe Mode, which makes any detected devices are considered 'safe' and should be added to the database of known devices\
        2. Standby Mode, which stops the program from detecting devices\
        3. Sentry Mode, where all bluetooth devices detected are checked against the db to see if they are new
      
