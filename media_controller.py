import cv2
import time
import numpy as np
import mediapipe as mp
import pyautogui
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- CONFIGURAÇÃO ---
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0) # Tente 1 se não abrir
cap.set(3, wCam)
cap.set(4, hCam)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# --- ÁUDIO ---
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
except:
    print("Erro de Áudio")

# --- VARIÁVEIS ---
volBar = 400
volPer = 0
last_action_time = 0   
ACTION_DELAY = 1.2     # Tempo de espera entre ações
msg_tela = ""          
msg_tempo_inicio = 0   
DURACAO_MSG = 2.0      

print("🎵 MEDIA CONTROLLER v5.0")
print("⚠️ REGRA: O volume só funciona se o dedo MÉDIO, ANELAR e MINDINHO estiverem LEVANTADOS.")

while True:
    success, img = cap.read()
    if not success: continue

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if time.time() - msg_tempo_inicio > DURACAO_MSG:
        msg_tela = ""

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            if len(lmList) != 0:
                # Pontos Principais
                x_thumb, y_thumb = lmList[4][1], lmList[4][2]
                x_index, y_index = lmList[8][1], lmList[8][2]
                x_pinky, y_pinky = lmList[20][1], lmList[20][2]
                
                # --- VERIFICAÇÃO DE "DEDOS ANTENA" (Esticados) ---
                # Se a ponta do dedo (TIP) está acima da articulação (PIP/MCP)
                # No OpenCV, Y menor é mais alto na tela.
                
                middle_up = lmList[12][2] < lmList[10][2]  # Médio esticado?
                ring_up   = lmList[16][2] < lmList[14][2]  # Anelar esticado?
                pinky_up  = lmList[20][2] < lmList[18][2]  # Mindinho esticado?
                
                # O volume só é permitido se esses 3 estiverem para cima
                VOLUME_SAFE_MODE = middle_up and ring_up and pinky_up

                # --- DISTÂNCIAS ---
                dist_vol = hypot(x_index - x_thumb, y_index - y_thumb)
                dist_next = hypot(x_pinky - x_thumb, y_pinky - y_thumb)

                # --- DETECÇÃO DE MÃO FECHADA (Soco) ---
                fingers_down = []
                for tip, base in zip([8, 12, 16, 20], [5, 9, 13, 17]):
                    fingers_down.append(lmList[tip][2] > lmList[base][2])
                is_fist = all(fingers_down)

                # --- BLOQUEIO DE VOLUME ---
                gesture_lock = is_fist or dist_next < 40


                # --- LÓGICA DE PRIORIDADE ---
                em_cooldown = (time.time() - last_action_time) < ACTION_DELAY

                # 1. PLAY/PAUSE (Soco)
                if is_fist and not em_cooldown:
                    pyautogui.press('playpause')
                    last_action_time = time.time()
                    msg_tela = "PLAY / PAUSE"
                    msg_tempo_inicio = time.time()
                    time.sleep(0.15)
                    cv2.circle(img, (lmList[9][1], lmList[9][2]), 40, (0, 0, 255), cv2.FILLED)
                
                # 2. NEXT TRACK (Mindinho + Dedão)
                # (Ignora se for punho fechado)
                elif dist_next < 40 and not is_fist and not em_cooldown:
                    pyautogui.press('nexttrack')
                    last_action_time = time.time()
                    msg_tela = ">> NEXT TRACK"
                    msg_tempo_inicio = time.time()
                    time.sleep(0.15)
                    cv2.circle(img, (x_thumb, y_thumb), 25, (0, 255, 255), cv2.FILLED)

                # 3. VOLUME (Só se SAFE_MODE for True)
                else:
                    if not em_cooldown and VOLUME_SAFE_MODE and not gesture_lock:
                        # Modo Ativo (Linha ROSA)
                        if dist_vol < 220:
                            cv2.line(img, (x_thumb, y_thumb), (x_index, y_index), (255, 0, 255), 3)
                            vol = np.interp(dist_vol, [30, 200], [minVol, maxVol])
                            volBar = np.interp(dist_vol, [30, 200], [400, 150])
                            volPer = np.interp(dist_vol, [30, 200], [0, 100])
                            volume.SetMasterVolumeLevel(vol, None)
                            msg_tela = f"Volume: {int(volPer)}%"
                            msg_tempo_inicio = time.time()
                    else:
                        # Modo Travado (Linha CINZA) - Feedback visual
                        if dist_vol < 220:
                            cv2.line(img, (x_thumb, y_thumb), (x_index, y_index), (100, 100, 100), 2)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # --- DESENHO HUD ---
    def draw_overlay(img, x, y, w, h, color=(0, 0, 0), alpha=0.5):
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    draw_overlay(img, 40, 140, 60, 270, (50, 50, 50), 0.6)
    cv2.rectangle(img, (40, 140), (100, 410), (0, 255, 0), 2)
    altura_barra = int(np.interp(volPer, [0, 100], [410, 140]))
    cv2.rectangle(img, (45, altura_barra), (95, 405), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (35, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

    if msg_tela != "":
        draw_overlay(img, 0, 0, 640, 80, (0, 0, 0), 0.7)
        text_size = cv2.getTextSize(msg_tela, cv2.FONT_HERSHEY_DUPLEX, 1.5, 2)[0]
        text_x = (640 - text_size[0]) // 2
        cor_texto = (0, 255, 255) 
        if "PAUSE" in msg_tela: cor_texto = (0, 0, 255) 
        if "Volume" in msg_tela: cor_texto = (0, 255, 0) 
        cv2.putText(img, msg_tela, (text_x, 55), cv2.FONT_HERSHEY_DUPLEX, 1.5, cor_texto, 2)
    
    cv2.imshow("Media Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()