import cv2 as cv
import mediapipe as mp
import time


password = [0, 1, 0, 0, 1]

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

cap = cv.VideoCapture(0)
print("Show Your Hand Broo!!!!")
time.sleep(3)


def get_fingers(hand_landmarks):
    fingers = []
    tips = [4, 8, 12, 16, 20]

   
    for i in range(1, 5):
        fingers.append(int(hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i] - 2].y))

   
    fingers.insert(0, int(hand_landmarks.landmark[tips[0]].x > hand_landmarks.landmark[tips[0] - 1].x))

    return fingers


def check_password(fingers):
    return "PASSWORD ACCEPTED!!" if fingers == password else "THAPPU DA!!"


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv.flip(frame, 1)
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
           
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = get_fingers(hand_landmarks)
            status = check_password(fingers)

            cv.putText(frame, f"Gesture: {fingers}", (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 5), 3)
            cv.putText(frame, status, (10, 80), cv.FONT_HERSHEY_SIMPLEX, 1.0,
                       (0, 255, 0) if "ACCEPTED" in status else (0, 0, 255), 3)

    else:
        cv.putText(frame, "no hand detected!", (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

   
    cv.imshow("Password Check", frame)

    if cv.waitKey(2) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
