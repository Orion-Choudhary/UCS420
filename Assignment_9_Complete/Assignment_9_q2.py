import cv2
from deepface import DeepFace

# initialize webcam feed
cap = cv2.VideoCapture(0)

# define cognitive adaptation policy based on detected mood
policy = {
    "happy": "You seem energetic. Cognitive computing is the key to happiness.",
    "sad": "Fatigue or low mood detected. Wanna scroll some reels?",
    "angry": "Remember, fighting is never the answer unless you are Utkarsh",
    "neutral": "Cognitive assistant standby. Smile for me.",
    "surprise": "Unexpected event detected. Mind sharing what you are excited about?",
    "fear": "High stress detected. Alexa, play Hanuman Chalisa!"
}

frame_count = 0
emotion = "neutral"
message = policy[emotion]
box = (0, 0, 0, 0)

while True:
    # capture live frame
    ret, frame = cap.read()
    frame_count += 1

    # sample emotion every 20 frames to maintain smooth 30 fps video
    if frame_count % 20 == 0:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        message = policy.get(emotion, "Standby.")
        region = result[0]['region']
        box = (region['x'], region['y'], region['w'], region['h'])

    # unpack bounding box coordinates
    x, y, w, h = box

    # draw face bounding box if detected
    if w > 0:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # render cognitive assistant status overlay
    cv2.putText(frame, f"State: {emotion}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, message, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # display interactive window
    cv2.imshow("Emotion Cognitive Assistant", frame)

    # press q to terminate session
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cleanup camera resources
cap.release()
cv2.destroyAllWindows()