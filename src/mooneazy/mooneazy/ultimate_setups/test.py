from alerts import sounds
import time

while True:
    sounds.play_alert()
    print("Playing alert sound...")
    time.sleep(5) 
    
     # Sleep for a second to avoid flooding the output    
     # pyinstaller --onefile --add-data "buzzer.wav;." test.py   
     # pyinstaller --onefile --add-data "buzzer.wav;." test.py