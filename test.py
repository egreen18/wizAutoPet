from tools import recordSequence, loadCoords, osResGen
import cv2
import numpy as np


os_res = osResGen()
coords = loadCoords(os_res)
memory = recordSequence(2, coords)

print(len(memory))

cv2.imshow("name", np.array(memory[0]))
cv2.waitKey(0)