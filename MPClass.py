import cv2
import mediapipe as mp

class Hands:
    def __init__(self, maxHands = 2, detection = 0.5, tracking = 0.5):
        self.hands= mp.solutions.hands.Hands(model_complexity = 0, max_num_hands = maxHands, min_detection_confidence = detection, min_tracking_confidence = tracking)
        self.handsDrawing = mp.solutions.drawing_utils

    def Marks(self, frame, height, width, depth = 1, handColor = (0, 0, 0)):
        HandDatas = {"left": [], "right": []}
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for left_OR_right, handData in zip (results.multi_handedness, results.multi_hand_landmarks):
                whichHand = left_OR_right.classification[0].label
                points = []
                for landMark in handData.landmark:
                    points.append((int(landMark.x * width), int(landMark.y * height), int(landMark.z * depth)))
                
                if whichHand == "Right":
                    HandDatas["right"] = points
                elif whichHand == "Left":
                    HandDatas["left"] = points
                '''
                # 根據手部偵測結果，標記手部節點和骨架
                self.handsDrawing.draw_landmarks(
                    frame, handData, mp.solutions.hands.HAND_CONNECTIONS, 
                    self.handsDrawing.DrawingSpec(color = handColor, thickness = 2, circle_radius = 4),
                    self.handsDrawing.DrawingSpec(color = handColor, thickness = 2, circle_radius = 2),
                )
                '''
        return HandDatas

class Pose:
    def __init__(self, detection = 0.5, tracking = 0.5):
        self.pose = mp.solutions.pose
        self.Pose = self.pose.Pose(min_detection_confidence=detection, 
                                           min_tracking_confidence = tracking)
        self.poseDrawing = mp.solutions.drawing_utils
        self.drawingStyle = mp.solutions.drawing_styles   
    
    def Marks(self, frame, height, width, depth):
        PoseData = []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.Pose.process(frameRGB)
        if result.pose_landmarks:
            for p in result.pose_landmarks.landmark:
                PoseData.append((int(p.x * width), int(p.y * height), int(p.z * depth)))
        # 根據姿勢偵測結果，標記身體節點和骨架
        '''
        self.poseDrawing.draw_landmarks(
            frame,
            result.pose_landmarks,
            self.pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.drawingStyle.get_default_pose_landmarks_style())
        '''
        return PoseData