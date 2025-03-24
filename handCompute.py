import numpy as np, math
import numpy as np
import math
import cv2

def compute(landmarks):
    parameters = []
    refp1 = np.array([landmarks[7][0], landmarks[7][1]])
    refp2 = np.array([landmarks[8][0], landmarks[8][1]])
    refDistance =  np.linalg.norm(refp2 - refp1)
    
    # Define pairs for distance calculation
    pairs = [(2, 4), (0, 4),
            (6, 8), (5, 8),
            (10, 12), (9, 12),
            (14, 16), (13, 16),
            (18, 20), (17, 20),

            (4, 8), (8, 12), (12, 16), (16, 20),
             
            (4, 5), (8, 9), (12, 13), (16, 17),
            (1, 8), (5, 12), (9, 16), (13, 20)]
    
    
    for pair in pairs:
        p1 = np.array([landmarks[pair[0]][0], landmarks[pair[0]][1]])
        p2 = np.array([landmarks[pair[1]][0], landmarks[pair[1]][1]])
        distance = np.linalg.norm(p2 - p1) / refDistance
        parameters.append(distance)
    
    finger_angle = fingerAngle(landmarks)
    for angle in finger_angle:
        parameters.append(angle)

    return parameters

def vector_angle(v1, v2):

    v1_x, v1_y, = v1
    v2_x, v2_y, = v2
    try:
        angle = math.degrees(math.acos((v1_x*v2_x + v1_y*v2_y) / (
            ((v1_x**2 + v1_y**2)**0.5) * ((v2_x**2 + v2_y**2)**0.5)
        )))
    except:
        angle = 180
    
    return angle

def vecter_compute(p1, p2):
    v1 = int(p1[0]) - int(p2[0])
    v2 = int(p1[1]) - int(p2[1])
    return (v1, v2)

# 根據傳入的 21 個節點座標，得到該手指的角度
def fingerAngle(hand_):
    angle_list = []
    
    # thumb 大拇指角度
    angle_ = vector_angle(vecter_compute(hand_[1], hand_[2]), vecter_compute(hand_[2], hand_[4]))
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_angle(vecter_compute(hand_[5], hand_[6]), vecter_compute(hand_[6], hand_[8]))
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_angle(vecter_compute(hand_[9], hand_[10]), vecter_compute(hand_[10], hand_[12]))
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_angle(vecter_compute(hand_[13], hand_[14]), vecter_compute(hand_[14], hand_[16]))
    angle_list.append(angle_)
    # little 小指角度
    angle_ = vector_angle(vecter_compute(hand_[17], hand_[18]), vecter_compute(hand_[18], hand_[20]))
    angle_list.append(angle_)
    
    return angle_list

def fingerPlay(angles):
    pick = []
    if angles[0] > 25:
        pick.append(0)
    if angles[1] > 30:
        pick.append(1)
    if angles[2] > 20:
        pick.append(2)
    if angles[3] > 20:
        pick.append(3)
    if angles[4] > 20:
        pick.append(4)
    return pick