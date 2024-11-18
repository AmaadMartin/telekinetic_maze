# utils/HandInput.py
import cv2
import mediapipe as mp
import numpy as np


class HandInput:
    def __init__(self):
        # Initialize video capture and mediapipe hands
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.right_hand_actions = {
            "Index": None,
            "Middle": None,
            "Ring": None,
            "Pinky": None,
        }
        self.left_hand_actions = {"Index": None}
        self.prev_positions = {"Right": None, "Left": None}

    def get_finger_name(self, landmark_id):
        """
        Returns the finger name based on the landmark ID.
        """
        finger_names = {4: "Thumb", 8: "Index", 12: "Middle", 16: "Ring", 20: "Pinky"}
        return finger_names.get(landmark_id, None)

    def detect_pinches(self, hand_landmarks, handedness):
        """
        Detects pinches between the thumb and other fingers.
        """
        thumb_tip = hand_landmarks.landmark[4]
        pinch_detected = {}
        for landmark_id in [8, 12, 16, 20]:  # Index, Middle, Ring, Pinky
            finger_tip = hand_landmarks.landmark[landmark_id]
            distance = np.linalg.norm(
                np.array([thumb_tip.x, thumb_tip.y])
                - np.array([finger_tip.x, finger_tip.y])
            )
            # Threshold for detecting pinch (adjust as needed)
            if distance < 0.05:
                finger_name = self.get_finger_name(landmark_id)
                pinch_detected[finger_name] = True
        return pinch_detected

    def get_actions(self):
        """
        Processes the camera feed and detects hand gestures.
        Returns a dictionary of actions.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Flip the image horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the image and find hands
        results = self.hands.process(image)
        # Convert the image color back so it can be displayed
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        actions = {"Right": {}, "Left": {}}

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                hand_label = handedness.classification[0].label  # 'Left' or 'Right'
                pinch_detected = self.detect_pinches(hand_landmarks, hand_label)
                actions[hand_label].update(pinch_detected)

        return actions

    def get_movement_direction(self, hand_label):
        """
        Determines the movement direction based on hand movement.
        Returns a tuple (dx, dy).
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                label = handedness.classification[0].label  # 'Left' or 'Right'
                if label == hand_label:
                    wrist = hand_landmarks.landmark[0]
                    wrist_pos = np.array([wrist.x, wrist.y])
                    if self.prev_positions[label] is not None:
                        delta = wrist_pos - self.prev_positions[label]
                        dx, dy = delta[0], delta[1]
                        threshold = 0.05  # Adjust as needed
                        if abs(dx) > abs(dy):
                            if dx > threshold:
                                direction = (1, 0)  # Right
                            elif dx < -threshold:
                                direction = (-1, 0)  # Left
                            else:
                                direction = None
                        else:
                            if dy > threshold:
                                direction = (0, 1)  # Down
                            elif dy < -threshold:
                                direction = (0, -1)  # Up
                            else:
                                direction = None
                        self.prev_positions[label] = wrist_pos
                        return direction
                    else:
                        self.prev_positions[label] = wrist_pos
        return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
