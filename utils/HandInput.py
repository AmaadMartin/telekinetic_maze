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
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils
        self.prev_center = None
        self.direction = None

    def is_hand_closed(self, hand_landmarks):
        """
        Determines if the hand is closed based on the positions of the fingertips and their corresponding PIP joints.
        """
        # Tip IDs for fingers (excluding thumb)
        tip_ids = [8, 12, 16, 20]
        fingers_closed = 0
        for tip_id in tip_ids:
            # Tip landmark
            tip = hand_landmarks.landmark[tip_id]
            # PIP joint (one joint before tip)
            pip = hand_landmarks.landmark[tip_id - 2]
            if tip.y > pip.y:
                fingers_closed += 1
        # If all four fingers are closed
        return fingers_closed == 4

    def get_hand_center(self, hand_landmarks):
        """
        Calculates the center of the hand based on the average position of the landmarks.
        """
        x_list = [landmark.x for landmark in hand_landmarks.landmark]
        y_list = [landmark.y for landmark in hand_landmarks.landmark]
        center_x = int(np.mean(x_list) * self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        center_y = int(np.mean(y_list) * self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (center_x, center_y)

    def get_direction(self):
        """
        Starts the video capture and processes frames to detect hand gestures and movements.
        Returns the movement direction when detected.
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            # Flip the image horizontally for a selfie-view display
            frame = cv2.flip(frame, 1)
            # Convert the BGR image to RGB.
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Process the image and find hands
            results = self.hands.process(image)
            # Convert the image color back so it can be displayed
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                # Assume only one hand is detected
                hand_landmarks = results.multi_hand_landmarks[0]
                # Draw landmarks
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                # Check if the hand is closed
                if self.is_hand_closed(hand_landmarks):
                    # Start recording movement
                    center = self.get_hand_center(hand_landmarks)
                    if self.prev_center is not None:
                        dx = center[0] - self.prev_center[0]
                        dy = center[1] - self.prev_center[1]
                        abs_dx = abs(dx)
                        abs_dy = abs(dy)
                        # Check if the movement exceeds a threshold to avoid noise
                        threshold = 20  # Pixels
                        if abs_dx > threshold or abs_dy > threshold:
                            if abs_dx > abs_dy:
                                if dx > 0:
                                    self.direction = 'Right'
                                else:
                                    self.direction = 'Left'
                            else:
                                if dy > 0:
                                    self.direction = 'Down'
                                else:
                                    self.direction = 'Up'
                    self.prev_center = center
                else:
                    self.prev_center = None
            else:
                self.prev_center = None

            # Display the resulting frame (optional, can be commented out)
            cv2.imshow('HandInput', image)

            if self.direction:
                print('Direction:', self.direction)
                temp_direction = self.direction
                self.direction = None
                self.prev_center = None
                return temp_direction

            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    hand_input = HandInput()
    while(True):
        hand_input.get_direction()