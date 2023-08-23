import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

click = 0
modo_game = 0
game = False

right = 0
left = 0
up = 0
down = 0
space = 0
s=0

TAM_TELA_X = 1920
TAM_TELA_Y = 1080
X_Y_INI = 100
aspect_ratio_screen = (TAM_TELA_X)/(TAM_TELA_Y)
prev_frame_time = 0
new_frame_time = 0


color_mouse_pointer = (0, 0, 255)


cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue


        #Processamento da imagem
        image.flags.writeable = False
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


        #Results recebe o processamento da imagem
        results = hands.process(image_rgb)

        #Converte novamente para vizualização
        image.flags.writeable = True
        image = cv2.resize(image, (960, 720), interpolation=cv2.INTER_NEAREST)
        height, width, _ = image.shape

        new_frame_time = time.time() 
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)


        if game == False:

            width_usable = width - X_Y_INI * 2
            height_usable = int(width_usable/aspect_ratio_screen)
            aux_image = np.zeros(image.shape, np.uint8)
            aux_image = cv2.rectangle(aux_image, (X_Y_INI, X_Y_INI), (X_Y_INI + width_usable, X_Y_INI + height_usable), (0,36,255), -1)
            image_mouse = cv2.addWeighted(image, 1, aux_image, 0.2, 0)
            cv2.putText(image_mouse, "MODO MOUSE", (20, 50), cv2.FONT_ITALIC, 1, (0, 36, 255), 2)
            cv2.putText(image_mouse, str(fps), (900, 50), cv2.FONT_ITALIC, 1, (0, 36, 255), 2)


            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:

                    ## Indicador
                    x1 = int(hand_landmarks.landmark[8].x * width)
                    y1 = int(hand_landmarks.landmark[8].y * height)
                    xm = np.interp(x1, (X_Y_INI, X_Y_INI + width_usable), (0, 1920))
                    ym = np.interp(y1, (X_Y_INI, X_Y_INI + height_usable), (0, 1080))
                    cv2.circle(image_mouse, (x1, y1), 10, color_mouse_pointer, 3)
                    cv2.circle(image_mouse, (x1, y1), 5, color_mouse_pointer, -1)

                    ## Mover Mouse
                    pyautogui.moveTo(int(xm), int(ym), 0, pyautogui.easeInOutQuad)  # start slow, end fast

                    ## Polegar
                    x2 = int(hand_landmarks.landmark[4].x * width)
                    y2 = int(hand_landmarks.landmark[4].y * height)
                    cv2.circle(image_mouse, (x2, y2), 10, color_mouse_pointer, 3)
                    cv2.circle(image_mouse, (x2, y2), 5, color_mouse_pointer, -1)


                    ## Ponto 5 Palma
                    x3 = int(hand_landmarks.landmark[5].x * width)
                    y3 = int(hand_landmarks.landmark[5].y * height)
                    cv2.circle(image_mouse, (x3, y3), 10, color_mouse_pointer, 3)
                    cv2.circle(image_mouse, (x3, y3), 5, color_mouse_pointer, -1)

                    ## Ponto 4 Palma
                    x4 = int(hand_landmarks.landmark[9].x * width)
                    y4 = int(hand_landmarks.landmark[9].y * height)

                    ## Dedo Médio
                    x5 = int(hand_landmarks.landmark[12].x * width)
                    y5 = int(hand_landmarks.landmark[12].y * height)
                    cv2.circle(image_mouse, (x5, y5), 10, color_mouse_pointer, 3)
                    cv2.circle(image_mouse, (x5, y5), 5, color_mouse_pointer, -1)

                    ## Anelar
                    x6 = int(hand_landmarks.landmark[16].x * width)
                    y6 = int(hand_landmarks.landmark[16].y * height)
                    cv2.circle(image_mouse, (x6, y6), 10, color_mouse_pointer, 3)
                    cv2.circle(image_mouse, (x6, y6), 5, color_mouse_pointer, -1)

                    ## Dedo Mindinho
                    x7 = int(hand_landmarks.landmark[20].x * width)
                    y7 = int(hand_landmarks.landmark[20].y * height)
                    cv2.circle(image_mouse, (x7, y7), 10, color_mouse_pointer, 3)
                    cv2.circle(image_mouse, (x7, y7), 5, color_mouse_pointer, -1)



                    if ((1.05 > x2/x3 > 0.95) and (1.05 > y2/y3 > 0.95)) or (((1.05 > x2/x4 > 0.95) and (1.3 > y2/y4 > 0.7))) :
                        click += 1
                        if click == 3:
                            print('click')
                            pyautogui.click()
                            click = 0

                    elif  y1!=0:
                        if (y5/y1 > 1.2) and (y6/y1 > 1.2) and (y5/y7 > 1.2):
                            modo_game += 1
                            if modo_game == 10 and game == False:
                                game = True
                                print('Modo Jogo Ativado')
                                modo_game = 0

            cv2.imshow('MediaPipe Hands', image_mouse)

        if game == True:


            ##Comando para desenhar as formas na tela
            aux_image = np.zeros(image.shape, np.uint8)
            aux_image = cv2.rectangle(aux_image, (575, 350), (675, 450), (128, 128, 128), -1)

            cv2.putText(image, "MODO JOGO", (20, 50), cv2.FONT_ITALIC, 1, (0, 36, 255), 2)
            cv2.putText(image, str(fps), (900, 50), cv2.FONT_ITALIC, 1, (0, 36, 255), 2)

            cv2.putText(aux_image, "<", (600, 420), cv2.FONT_ITALIC, 2, 0, 4)

            cv2.rectangle(aux_image, (750, 350), (850, 450), (128, 128, 128), -1)
            cv2.putText(aux_image, ">", (775, 420), cv2.FONT_ITALIC, 2, 0, 4)

            cv2.rectangle(aux_image, (662, 225), (762, 325), (128, 128, 128), -1)
            cv2.putText(aux_image, "^", (690, 290), cv2.FONT_ITALIC, 2, 0, 4)

            cv2.rectangle(aux_image, (662, 475), (762, 575), (128, 128, 128), -1)
            cv2.putText(aux_image, "v", (695, 540), cv2.FONT_ITALIC, 2, 0, 4)

            cv2.rectangle(aux_image, (150, 350), (350, 450), (128, 128, 128), -1)
            cv2.putText(aux_image, "Espaco", (175, 420), cv2.FONT_ITALIC, 1, 0, 4)

            cv2.rectangle(aux_image, (200, 225), (300, 325), (128, 128, 128), -1)
            cv2.putText(aux_image, "s", (225, 290), cv2.FONT_ITALIC, 2, 0, 4)   


            image_game = cv2.addWeighted(image, 1, aux_image, 1, 0)

            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:

                    ## Indicador
                    x1 = int(hand_landmarks.landmark[8].x * width)
                    y1 = int(hand_landmarks.landmark[8].y * height)
                    cv2.circle(image_game, (x1, y1), 10, color_mouse_pointer, 3)
                    cv2.circle(image_game, (x1, y1), 5, color_mouse_pointer, -1)


                    ## Dedo Médio
                    x5 = int(hand_landmarks.landmark[12].x * width)
                    y5 = int(hand_landmarks.landmark[12].y * height)
                

                    ## Anelar
                    x6 = int(hand_landmarks.landmark[16].x * width)
                    y6 = int(hand_landmarks.landmark[16].y * height)


                    ## Dedo Mindinho
                    x7 = int(hand_landmarks.landmark[20].x * width)
                    y7 = int(hand_landmarks.landmark[20].y * height)


                    if x1>480:
                        #Botão Esquerdo
                        if (575 < x1 < 675) and (350 < y1 < 450):
                            if left == 0:
                                pyautogui.keyDown('left')
                                print('left')
                                left = 1

                        #Botão Direito
                        elif (750 < x1 < 850) and (350 < y1 < 450):
                            if right == 0:
                                pyautogui.keyDown('right')
                                print('right')
                                right = 1

                        # Botão Cima
                        elif (662 < x1 < 762) and (225 < y1 < 325):
                            if up == 0:
                                pyautogui.keyDown('up')
                                print('up')
                                up = 1

                        # Botão Baixo
                        elif (662 < x1 < 762) and (475 < y1 < 575):
                            if down == 0:
                                pyautogui.keyDown('down')
                                print('down')
                                down = 1

                        elif (y1!=0) and (y5/y1 > 1.2) and (y6/y1 > 1.2) and (y5/y7 > 1.2):
                            if (modo_game == 10 and game == True):
                                game = False
                                print('Modo Jogo Desativado')
                                modo_game = 0
                            modo_game += 1

                        else:
                            if left == 1:
                                pyautogui.keyUp('left')
                                left = 0

                            elif right == 1:
                                pyautogui.keyUp('right')
                                right = 0 

                            elif up == 1:
                                pyautogui.keyUp('up')
                                up = 0

                            elif down == 1:
                                pyautogui.keyUp('down')
                                down = 0

                
                    elif x1<480:
                        # Botão Espaço
                        if (150 < x1 < 350) and (350 < y1 < 450):
                            if space == 0:
                                pyautogui.keyDown('space')
                                print('space')
                                space = 1

                        # Botão S
                        elif (200 < x1 < 300) and (225 < y1 < 325):
                            if s == 0:
                                pyautogui.keyDown('s')
                                print('s')
                                s = 1

                        elif (y1!=0) and (y5/y1 > 1.2) and (y6/y1 > 1.2) and (y5/y7 > 1.2):
                            if (modo_game == 10 and game == True):
                                game = False
                                print('Modo Jogo Desativado')
                                modo_game = 0
                            modo_game += 1

                        else:
                            if space == 1:
                                pyautogui.keyUp('space')
                                space = 0

                            elif s == 1:
                                pyautogui.keyUp('s')
                                s = 0


            cv2.imshow('MediaPipe Hands', image_game)

        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()




