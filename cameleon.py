#!/usr/bin/python3

import os
import cv2
import json

class Camera:
    def __init__(self) -> None:
        '''Represents a camera instance.'''
        
        self.video = cv2.VideoCapture(0)
        
        self.static_back = None
        self.motion_list = [None, None]
        self.time = []
        
        self.dbg = False
    
    def start(self, show_image: bool = False, on_motion: callable = None,
              show_motion: bool = True) -> None:
        '''Start the camera.'''
        
        while 1:
            _, frame = self.video.read()
            motion = 0
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
            if self.static_back is None:
                self.static_back = gray
                continue
            
            diff_frame = cv2.absdiff(self.static_back, gray)
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
            
            cnts, _ = cv2.findContours(
                thresh_frame.copy(),
                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
    
            for contour in cnts:
                if cv2.contourArea(contour) < 10000: continue
                motion = 1
            
                (x, y, w, h) = cv2.boundingRect(contour)
            
                # making green rectangle around the moving object
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            self.motion_list.append(motion)
            self.motion_list = self.motion_list[-2:]
            
            # Call on motion
            if on_motion is not None:
                if all(self.motion_list): on_motion()
            
            # Show camera on screen
            if show_image: cv2.imshow("Cameleon", frame)
            
            # Quit key
            if cv2.waitKey(1) == ord('q'): break
            
            if not self.dbg:
                print('Cameleon ready. o7')
                self.dbg = True
        
        self.video.release()
        
        # Destroying all the windows
        cv2.destroyAllWindows()

settings = json.load(open('settings.json', 'r'))
pause, group, command = settings.values()

def disparition() -> None:
    '''Camaleon go byeee'''
    
    if pause: os.popen('playerctl pause')                               # Pause current track
    if group is not None: os.popen(f'xdotool set_desktop {group - 1}')  # Switch to group nth
    if command is not None: os.popen(command)                           # Execute command
    
    # Debug and Exit
    print('AHHHHHHHH')
    raise SystemExit()


if __name__ == '__main__':
    
    cam = Camera()
    
    try: cam.start(on_motion = disparition)
    except KeyboardInterrupt:
        os.popen('notify-send "Cameleon" "Cameleon has seen nothing. Be prudent, tho!"')
        print('Service stopped.')
