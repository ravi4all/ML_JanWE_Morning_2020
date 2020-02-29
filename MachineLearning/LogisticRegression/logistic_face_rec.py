import cv2
import pickle as pkl
import numpy as np
from sklearn.model_selection import train_test_split

face_1 = np.load('face_1.npy')
face_1 = face_1.reshape((200,-1))

face_2 = np.load('face_2.npy')
face_2 = face_2.reshape((200,-1))

faceData = np.concatenate([face_1,face_2])
faceData = faceData/255
labels = np.zeros((faceData.shape[0],1))
labels[200:,:] = 1.0

def predict(row,coef):
    x = coef[0]
    for i in range(len(row) - 1):
        x += coef[i+1] * row[i]
    return 1 / (1 + np.exp(-x))

def accuracy_metrics(actual,prediction):
    count = 0
    for i in range(len(actual)):
        if actual[i] == prediction[i]:
            count += 1
    return count/len(actual) * 100

def gradientDescent(x_train,y_train,epochs,alpha):
    coef = np.zeros(x_train.shape[1] + 1)
    n = len(x_train)
    for i in range(epochs):
        # predictions = []
        for j in range(len(x_train)):
            pred = predict(x_train[j],coef)
            error = pred - y_train[j]
            coef[0] = coef[0] - alpha * (1/n) * np.sum(error)
            for k in range(len(x_train[0] - 1)):
                coef[k+1] = coef[k+1] - alpha * (1/n) * np.dot(x_train[j][k],error)

        print("{} Epochs Completed".format(i))
    return coef

def evaluateAlgorithm(epochs,alpha):
    x_train,x_test,y_train, y_test = train_test_split(faceData,labels,test_size=0.25)
    score = logistic(x_train,y_train,x_test,y_test,epochs,alpha)
    return score
    
def logistic(x_train,y_train,x_test,y_test,epochs,alpha):
    coef = gradientDescent(x_train,y_train,epochs,alpha)
    file = open('face_weights.pkl','wb')
    pkl.dump(coef,file)
    file.close()
    predictions = []
    for row in x_test:
        pred = predict(row,coef)
        predictions.append(round(pred))
    accuracy = accuracy_metrics(y_test,predictions)
    return accuracy

epochs = 50
alpha = 0.01

score = evaluateAlgorithm(epochs,alpha)
print(score)
