import numpy as np
import cv2

largura_min = 28  # Largura minima do retangulo
altura_min = 28  # Altura minima do retangulo
offset = 6  # Erro permitido entre pixel
pos_linha = 475  # Posição da linha de contagem
delay = 60  # FPS do vídeo
detec = []

cap = cv2.VideoCapture('example1.mp4')

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while(1):
    ret, frame = cap.read()

    
    fgmask = fgbg.apply(frame)
    
    fgmask = cv2.dilate(fgmask, np.ones((5, 5)))
        
    (cnt, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    fgmask = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #cv2.drawContours(frame, cnt, -1, (0, 255, 0), 2) #Desenha Contorno
        
    cv2.line(frame, (5, pos_linha), (1400, pos_linha), (0, 0, 255), 1)

    for (i, c) in enumerate(cnt):
        (x, y, w, h) = cv2.boundingRect(c)
        validar_contorno = (w >= largura_min) and (h >= altura_min)
        if not validar_contorno:
            continue

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    

cap.release()


cv2.destroyAllWindows()