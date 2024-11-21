# utils/HandInput.py
import cv2
import mediapipe as mp
import numpy as np

PINCH_THRESHOLD = 0.06
MOVE_THRESHOLD = 0.045

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
            if distance < PINCH_THRESHOLD:
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
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                hand_label = handedness.classification[0].label  # 'Left' or 'Right'
                pinch_detected = self.detect_pinches(hand_landmarks, hand_label)
                actions[hand_label].update(pinch_detected)

        # cv2.imshow("Hand Input", image)

        return actions
    
    def get_finger_direction(self, hand_label, finger_name):
        """
        Returns the direction of a finger based on hand movement.
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
                label = handedness.classification[0].label
                if label == hand_label:
                    finger_id = None
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        if self.get_finger_name(idx) == finger_name:
                            finger_id = idx
                            break
                    if finger_id is not None:
                        finger_pos = np.array([landmark.x, landmark.y])
                        if self.prev_positions[hand_label] is not None:
                            delta = finger_pos - self.prev_positions[hand_label]
                            dx, dy = delta[0], delta[1]
                            threshold = MOVE_THRESHOLD
                            if abs(dx) > abs(dy):
                                if dx > threshold:
                                    direction = (1, 0)
                                elif dx < -threshold:
                                    direction = (-1, 0)
                                else:
                                    direction = None
                            else:
                                if dy > threshold:
                                    direction = (0, 1)
                                elif dy < -threshold:
                                    direction = (0, -1)
                                else:
                                    direction = None
                            self.prev_positions[hand_label] = finger_pos
                            return direction
                        else:
                            self.prev_positions[hand_label] = finger_pos
        return None

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
                        threshold = MOVE_THRESHOLD  # Adjust as needed
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
                        print(direction)
                        return direction
                    else:
                        self.prev_positions[label] = wrist_pos
        return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
