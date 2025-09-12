"""
Fairdyne - Automated green soul movement using computer vision
This version uses OS-level keyboard events to control movement. It is easier to set up, but can be marginally slower.

Author: Powercube
"""

import cv2
import math
from mss import mss
import numpy as np
from keyboard import press_and_release as press
from tools import Directions

monitor = {"top": 155, "left": 560, "width": 800, "height": 600}
sct = mss()
soul_location = (319, 240)
last_direction = None

yellow = {
    "lower": np.array([20, 210, 0], dtype=np.uint8),
    "upper": np.array([30, 230, 255], dtype=np.uint8)
}
blue = {
    "lower": np.array([95, 200, 0], dtype=np.uint8),
    "upper": np.array([100, 215, 255], dtype=np.uint8)
}

while True:
    frame = np.array(sct.grab(monitor))
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, blue["lower"], blue["upper"])
    mask_yellow = cv2.inRange(hsv, yellow["lower"], yellow["upper"])
    mask = cv2.bitwise_or(mask_blue, mask_yellow)

    min_distance = float('inf')
    closest_coords = None

    contours = filter(lambda c: cv2.contourArea(c) > 40, cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0])
    for contour in contours:
        M = cv2.moments(contour)

        cX = round(M["m10"] / M["m00"])
        cY = round(M["m01"] / M["m00"])

        dx = cX - soul_location[0]
        dy = soul_location[1] - cY

        distance = math.hypot(dx, dy)
        if distance < min_distance:
            min_distance = distance
            closest_coords = (cX, cY)

        cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1)
        cv2.putText(frame, f"({cX}, {cY})", (cX + 10, cY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    if closest_coords is not None:
        dx = closest_coords[0] - soul_location[0]
        dy = soul_location[1] - closest_coords[1]
        angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360

        direction = Directions.get_closest_direction(angle)

        if direction != last_direction:
            press(direction.input_key)
            last_direction = direction

            cv2.putText(frame, f"Direction: {direction.name}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Angle: {angle:.2f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        last_direction = None

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

sct.close()
cv2.destroyAllWindows()