import keyboard
import mouse
import enum
from playsound import playsound
import time

class StrafeDir(enum.Enum):
    left = 1
    right = 2
    NA = 3

previous_pos = mouse.get_position()
strafe_dir = StrafeDir.NA
a_pushed = False
d_pushed = False

negative_sync_adj = 2
positive_sync_adj = 1
current_sync_score = 0
previous_sync_score = 0
bad_sync_threshold = 250
test_interval = .1
start_time = time.time()

while True:

    current_pos = mouse.get_position()
    counter_strafe = False
    good_strafe = False

    if current_pos[0] > previous_pos[0]:
        strafe_dir = StrafeDir.right
    elif current_pos[0] < previous_pos[0]:
        strafe_dir = StrafeDir.left
    else:
        strafe_dir = StrafeDir.NA

    previous_pos = current_pos
    
    if keyboard.is_pressed("a"):
        a_pushed = True
    else:
        a_pushed = False

    if keyboard.is_pressed("d"):
        d_pushed = True
    else:
        d_pushed = False
    
    if strafe_dir is StrafeDir.left:
        if d_pushed:
            counter_strafe = True
            print("D Pushed while strafing th wrong way")
        if a_pushed:
            good_strafe = True
            print("Good Strafe")
    if strafe_dir is StrafeDir.right:
        if a_pushed:
            counter_strafe = True
            print("A Pushed while strafing the wrong way")
        if d_pushed:
            good_strafe = True
            print("Good Strafe")
    if a_pushed and d_pushed:
        counter_strafe = True
        print("A and D Pushed")

    if counter_strafe:
        current_sync_score -= negative_sync_adj
    if good_strafe:
        current_sync_score += positive_sync_adj

    if time.time() - start_time > test_interval:
        if current_sync_score < previous_sync_score - bad_sync_threshold:
            playsound("pop.wav")
        elif current_sync_score > previous_sync_score:
            print("Good Sync")
        previous_sync_score = current_sync_score
        print("Sync: " + str(current_sync_score))
        start_time = time.time()