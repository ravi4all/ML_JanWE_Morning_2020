import cv2
import pickle as pkl

with open('cluster.pkl','rb') as file:
    clusters = pkl.load(file)

cascade = cv2.CascadeClassifier('cascade.xml')
img = cv2.imread('test_1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
face = cascade.detectMultiScale(gray,1.3)
# print(face)
x,y,w,h = face[0]
face = gray[y:y+h,x:x+w]
face = cv2.resize(face,(50,50))
face = face / 255.
pred = clusters.predict([face.flatten()])
print(pred)
