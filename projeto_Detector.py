import numpy as np
import cv2
from time import sleep

def set_info_direita(detecta):
    global carros_indo
    for (x, y) in detecta:
        if (pos_linha_direita + offset) > y > (pos_linha_direita - offset) and comp_linha_direita > x > 700:
            carros_indo += 1
            cv2.line(frame, (700, pos_linha_direita), (comp_linha_direita, pos_linha_direita), (0, 127, 255), 3)
            detecta.remove((x, y))
            print("Carros indo: " + str(carros_indo))
            
def set_info_esquerda(detecta):
    global carros_vindo
    for (x, y) in detecta:
        if (pos_linha_esquerda + offset) > y > (pos_linha_esquerda - offset) and comp_linha_esquerda > x > 200:
            carros_vindo += 1
            cv2.line(frame, (200, pos_linha_esquerda), (comp_linha_esquerda, pos_linha_esquerda), (0, 127, 255), 3)
            detecta.remove((x, y))
            print("Carros vindo: " + str(carros_vindo))

def pega_centro(x, y, largura, altura):

    x1 = largura // 2
    y1 = altura // 2
    cx = x + x1
    cy = y + y1
    return cx, cy

def texto(frame):
    carrosVindo = f'Carros Vindo: {carros_vindo}'
    carrosIndo = f'Carros Indo: {carros_indo}'
    relacaoIndoxVindo = "Iniciando..."
    if carros_vindo != 0:
        relacaoIndoxVindo = f'1 carro vindo para {round((carros_indo/carros_vindo),1)} carro indo'
    cv2.putText(frame, carrosVindo, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 127, 0), 3)
    cv2.putText(frame, carrosIndo, (1000, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 127, 0), 3)
    cv2.putText(frame, relacaoIndoxVindo, (350, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


#####CONSTANTES##########
largura_min = 25  # Largura minima do retangulo
altura_min = 25  # Altura minima do retangulo
offset = 1.5  # Erro permitido entre pixel

pos_linha_direita = 540  # Posição da linha de contagem
comp_linha_direita = 1250

pos_linha_esquerda = 540
comp_linha_esquerda = 615

delay = 30  # FPS do vídeo
detecta = []

carros_indo = 0
carros_vindo = 0
########################

cap = cv2.VideoCapture('example1.mp4')

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while(1):
    ret, frame = cap.read()

    sleep(float(1/delay))
                                                                             #############
    removefundo = fgbg.apply(frame)
    dilata = cv2.dilate(removefundo, np.ones((5, 5)))
    (cnt, hierarchy) = cv2.findContours(dilata.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)        ##TRATAMENTO DA IMAGEM
    fgmask = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                                     #############
                                                                                                        
        
    cv2.line(frame, (700, pos_linha_direita), (comp_linha_direita, pos_linha_direita), (255, 127, 0), 3)        ## CRIANDO LINHA DA DIREITA
    cv2.line(frame, (200, pos_linha_esquerda), (comp_linha_esquerda, pos_linha_esquerda), (255, 127, 0), 3)     ## CRIANDO LINHA DA ESQUERDA

    for (i, c) in enumerate(cnt):                                       #########################
        (x, y, w, h) = cv2.boundingRect(c)
        validar_contorno = (w >= largura_min) and (h >= altura_min)
        if not validar_contorno:                                                #DESENHA O RETANGULO
            continue
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)    ##########################
                                                                        
       
        centro = pega_centro(x, y, w, h)                                ##################
        detecta.append(centro)                                          #DETECTA O CENTRO
        
        

    set_info_direita(detecta)               #DETECTA SE O CENTRO DE CADA RETANGULO SE APROXIMA DA SUA RESPECTIVA LINHA DIREITA
    set_info_esquerda(detecta)              #DETECTA SE O CENTRO DE CADA RETANGULO SE APROXIMA DA SUA RESPECTIVA LINHA ESQUERDA
    
    texto(frame)

    cv2.imshow('frame',frame)
    
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    

cap.release()


cv2.destroyAllWindows()