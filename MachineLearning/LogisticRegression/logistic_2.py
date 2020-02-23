import csv, random
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

#def loadDataset(path):
#    data = []
#    with open(path) as file:
#        reader = csv.reader(file)
#        for row in reader:
#            data.append(row)
#    return data

def cross_validation(features,labels):
    dataset = np.c_[features,labels]
    data_copy = list(dataset)
    k = 5
    fold_size = len(dataset) // k
    folds = []
    for i in range(k):
        fold = []
        while len(fold) < fold_size:
            index = random.randrange(len(data_copy))
            fold.append(data_copy.pop(index))
        folds.append(fold)
    return folds

def prediction(row,coef):
    x = coef[0]
    for i in range(len(row) - 1):
        x += coef[i+1] * row[i]
    return 1 / (1 + math.exp(-x))

def accuracy(actual,pred):
    counter = 0
    for i in range(len(actual)):
        if actual[i] == pred[i]:
            counter += 1
    return counter / len(actual) * 100

def gradient(x_train,y_train,epochs,alpha):
    coef = [0] * x_train.shape[1] + 1
    n = x_train.shape[0]
    for i in range(epochs):
        for j in range(len(x_train)):
            pred = prediction(x_train[j],coef)
            loss = pred - y_train[j]
            grad = (1/n) * sum(loss)
            coef[0] = coef[0] - alpha * grad
            for k in range(len(x_train[j])):
                grad = (1/n) * np.dot(x_train[j],loss)
                coef[k+1] = coef[k+1] - alpha * grad
    return coef

def logisticRegression(x_train,y_train,x_test,y_test,epoch,alpha):
    coef = gradient(x_train,y_train,epochs,alpha)
    predictedList = []
    for row in x_test:
        pred = prediction(row,coef)
        predictedList.append(round(pred))
    return accuracy(y_test,predictedList)

def evaluate(folds,epochs,alpha):
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    acc = logisticRegression(x_train,y_train,x_test,y_test,epochs,alpha)
    return acc

fileName = 'Churn_Modelling.csv'    
dataset = pd.read_csv(fileName)

X = dataset.iloc[:,3:-1]
y = dataset.iloc[:,-1]

encoder = LabelEncoder()
X['Gender'] = encoder.fit_transform(X['Gender'])

X['Geography'] = encoder.fit_transform(X['Geography'])

onehot = OneHotEncoder(categorical_features=[1])
X = onehot.fit_transform(X).toarray()

normalize = MinMaxScaler()
X = normalize.fit_transform(X)

folds = cross_validation(X,y)

epochs = 1000
alpha = 0.01
scores = evaluate(folds,epochs,alpha)
print(scores)

#x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.25)
#
#reg = LogisticRegression()
#reg.fit(x_train,y_train)
#
#y_pred = reg.predict(x_test)
#accuracy_score(y_test,y_pred)
