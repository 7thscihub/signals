import os
import sys
import time


relative_path = os.path.join('alerts', 'buzzer.wav')
script_dir = os.path.dirname(os.path.abspath(__file__))
abs_path = os.path.join(script_dir, 'buzzer.wav')

# print("Full path:", abs_path)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(abs_path)


# print(resource_path(relative_path=relative_path))

from betterplaysound import playsound
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"



def play_alert():
    
    # alert_path = r'C:\Users\cassim\Desktop\DevNet\ultimatescript\alerts\buzzer.wav'
    alert_path = resource_path(relative_path=relative_path)
    count = 0
    while count < 25:
        playsound(alert_path)
        count += 1
        time.sleep(10)


if __name__ == "__main__":
    play_alert()
