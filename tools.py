import cv2
import numpy as np
from enum import Enum

class Recorder:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.fourcc = cv2.VideoWriter.fourcc(*"XVID")
        self.out = cv2.VideoWriter(self.output_file, self.fourcc, 60.0, (640, 480))

    def update(self, frame: np.ndarray):
        if frame.shape[1] != 640 or frame.shape[0] != 480:
            frame = cv2.resize(frame, (640, 480))
        self.out.write(frame)

    def release(self):
        self.out.release()

class Directions(Enum):
    angle: int
    input_key: str
    shield_direction: int

    def __new__(cls, angle, input_key, shield_direction):
        obj = object.__new__(cls)
        obj._value_ = angle
        
        obj.angle = angle
        obj.input_key = input_key
        obj.shield_direction = shield_direction
        return obj

    NORTH = (90, "w", 3)
    SOUTH = (270, "s", 1)
    EAST = (0, "d", 4)
    WEST = (180, "a", 2)

    @staticmethod
    def get_closest_direction(angle: float) -> 'Directions':
        return min(Directions, key=lambda dir: abs((angle - dir.angle + 180) % 360 - 180))

if __name__ == "__main__":
    print(str(Directions["NORTH"]))