#!/usr/bin/env python

import cv2
import numpy as np
import time

try:
    from PIL import ImageGrab
except:
    import pyscreenshot as ImageGrab
    
class Skype():
    def __init__(self, icon):
        self.skype = cv2.imread(icon)
        
    @staticmethod
    def has_image(haystack, needle):
        haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
        needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
        w, h = needle.shape[::-1]
        res = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
        threshold = 0.99
        loc = np.where(res >= threshold)
        try:
            assert loc[0] > 0
            assert loc[1] > 0
            return True
        except:
            return False
        
    @staticmethod
    def get_tray_bitmap(x, y, w, h):
        tray_area = ImageGrab.grab(bbox=(x, y, x+w, y+h))
        tray_area_data = np.array(tray_area)
        return tray_area_data[:, :, ::-1]
    
    def is_unseen(self):
        x, y, w, h = 1480, 1050, 440, 30
        tray = self.get_tray_bitmap(x, y, w, h)
        
        return self.has_image(tray, self.skype)
            
            
if __name__ == "__main__":
    s = Skype('skype.png')
    
    while True:
        if s.is_unseen():
            print "New message!"
        else:
            print "Meh! Nothing to do."
            
        time.sleep(0.5)