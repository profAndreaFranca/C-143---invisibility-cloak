import cv2
import time
import numpy as np

#Para salvar o resultado em um arquivo chamado output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Iniciando a webcam
cap = cv2.VideoCapture(0)

#Permitindo que a webcam inicie fazendo o código aguardar 2 segundos
time.sleep(2)
bg = 0

#Capturando o plano de fundo durante 60 quadros
for i in range(60):
    ret, bg = cap.read()
#Invertendo o plano de fundo
bg = np.flip(bg, axis=1)

#Lendo o quadro capturado até que a câmera esteja aberta
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break

    #Invertendo a imagem por motivo de consistência
    img = np.flip(img, axis=1)

    #Convertendo a cor de BGR para HSV
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #Gerando máscara para detectar a cor vermelha (os valores podem ser alterados)
    lowerRed = np.array([0,120,50])
    upperRed = np.array([10,255,255])
    mask1 = cv2.inRange(hsv,lowerRed,upperRed)
    lowerRed = np.array([170,120,70])
    upperRed= np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lowerRed,upperRed)
    #Abrindo e expandindo a imagem onde há a máscara 1 (cor)
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))

    #Selecionando apenas a parte que não possui máscara 1 e salvando-a na máscara 2
   
    mask2 = cv2.bitwise_not(mask1)
    

     #Mantendo apenas a parte das imagens sem a cor vermelha
    #(ou qualquer outra cor que você escolher)
    
    res1 = cv2.bitwise_and(img, img, mask = mask2)
   

    #Mantendo apenas a parte das imagens com a cor vermelha
   
    res2 = cv2.bitwise_and(bg,bg, mask = mask1)

    #Gerando o resultado final mesclando res_1 e res_2
    final_output = cv2.addWeighted(res1,1,res2,1,0)
    output_file.write(final_output)
    #Exibindo o resultado para o usuário
    cv2.imshow("capa de invisibilidade",final_output)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()
