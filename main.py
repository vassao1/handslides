import cv2
import mediapipe as mp
import gestos
import pyautogui
import time

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Erro: nao foi possivel abrir a camera")
    exit()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

ultimo_comando = 0
cooldown = 0.7
ultimo_gesto = None

while True:
    sucesso, frame = camera.read()

    if not sucesso:
        print("Erro: nao foi possivel ler o frame da camera")
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    resultado = hands.process(frame_rgb)

    if resultado.multi_hand_landmarks:
        for hand_landmarks in resultado.multi_hand_landmarks:
            juntas = hand_landmarks.landmark

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            agora = time.time()
            gesto = gestos.detectar_gestos(juntas)
            if gesto != ultimo_gesto and agora - ultimo_comando > cooldown:
                if gesto == "VOLTAR":
                    pyautogui.press('left')
                    ultimo_comando = agora
                elif gesto == "PASSAR":
                    pyautogui.press('right')
                    ultimo_comando = agora
                
                ultimo_gesto = gesto

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()