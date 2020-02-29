import cv2
import pickle as pkl
import numpy as np

cascade = cv2.CascadeClassifier('data.xml')

file = open('face_weights.pkl','rb')
weights = pkl.load(file)

def predict(row,coef):
    x = coef[0]
    for i in range(len(row) - 1):
        x += coef[i+1] * row[i]
    return 1 / (1 + np.exp(-x))

# img = cv2.imread('test_img.jpg')
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# face = cascade.detectMultiScale(gray,1.5)
# while True:
#     for x,y,w,h in face:
#         cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#         faceComp = gray[y:y+h,x:x+w]
#         faceComp = cv2.resize(faceComp,(50,50))
#         y_pred = predict(faceComp.flatten(),weights)
#         print(round(y_pred))
#     cv2.imshow('res',img)
#     if cv2.waitKey(1) == 27:
#         break
# cv2.destroyAllWindows()
    
cap = cv2.VideoCapture(0)
users = {
    0 : "Ravi",
    1 : "Sid"
}
font = cv2.FONT_HERSHEY_COMPLEX
while True:
    flag,img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray,1.5)
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        faceComp = gray[y:y+h,x:x+w]
        faceComp = cv2.resize(faceComp,(50,50))
        y_pred = predict(faceComp.flatten(),weights)
        lab = int(round(y_pred))
        name = users[lab]
        cv2.putText(img,name,(x,y),font,1,(255,255,0),2)
    cv2.imshow('res',img)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
cap.release()
