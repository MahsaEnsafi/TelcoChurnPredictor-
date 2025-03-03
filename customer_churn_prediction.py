# -*- coding: utf-8 -*-
"""Customer churn prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pU3XpOs9svjp7bXFDLWhZx9P8zBiC5jH
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report
import seaborn as sn
import tensorflow as tf
from tensorflow import keras



df=pd.read_csv('/content/drive/MyDrive/data/tutrial_tensorflow/Customer churn prediction/Telco-Customer-Churn.csv')
df.sample(5)  #Display four randomly selected rows

df.drop('customerID',axis=1,inplace=True) #customerID is not useful
df.sample(3)

df[pd.to_numeric(df.TotalCharges,errors='coerce').isnull()]
#Delete rows that have null values

#Delete rows that have blank values
df1=df[df.TotalCharges!=' ']
df1.shape

df1.dtypes

#Converting the data type of the 'TotalCharges' column from an object to a numerical format
df1.TotalCharges=pd.to_numeric(df1.TotalCharges)

df1.TotalCharges.dtype

#Visualizition
Partner_Churn_no=df1[df1.Churn=='No'].MonthlyCharges
Partner_Churn_yes=df1[df1.Churn=='Yes'].MonthlyCharges
plt.xlabel('MonthlyCharges')
plt.ylabel('Number')
plt.title('Visualizition')
plt.hist([Partner_Churn_no,Partner_Churn_yes],color=['red','green'],label=['churn=no','chrn=yes'])
plt.legend()

def show_column(df1):
  for column in df1:
    if df1[column].dtype=='object':
      print(column)
      print(df1[column].unique())

show_column(df1)

df1.replace('No phone service','No',inplace=True)
df1.replace('No internet service','No',inplace=True)
show_column(df1)

yes_no_columns=['Partner','Dependents','PhoneService','MultipleLines','OnlineSecurity','OnlineBackup','DeviceProtection',
'TechSupport','StreamingTV','StreamingMovies','PaperlessBilling','Churn']

dict_yes_no={'Yes':1,'No':0}
for col in yes_no_columns:
  df1[col].replace(dict_yes_no,inplace=True)
  print(col)
  print(df1[col].unique())

dict_fem_mal={'Female':1,'Male':0}
df1['gender'].replace(dict_fem_mal,inplace=True)
for col in df1:
  print(col)
  print(df1[col].unique())

df2=pd.get_dummies(data=df1,columns=['InternetService','Contract','PaymentMethod'],dtype=np.float64)
df2.columns

for col in df2:
  print(col)
  print(df2[col].unique())

df2.dtypes

scaler=MinMaxScaler()
colmns_to_scale=['tenure','MonthlyCharges','TotalCharges']
df2[colmns_to_scale]=scaler.fit_transform(df2[colmns_to_scale])

df2.sample(4)

X=df2.drop('Churn',axis=1)
Y=df2['Churn']

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=5)

print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

#creating and training model
model=keras.Sequential([
    keras.layers.Dense(26,input_shape=(26,),activation='relu'),
    keras.layers.Dense(100,activation='relu'),
    keras.layers.Dense(75,activation='relu'),
    keras.layers.Dense(50,activation='relu'),
    keras.layers.Dense(25,activation='relu'),
    keras.layers.Dense(1,activation='sigmoid')
])
model.compile(
    optimizer='adam',
    loss=keras.losses.BinaryCrossentropy,
    metrics=['accuracy']
)
model.fit(X_train,Y_train,epochs=100)

#evaluting model
model.evaluate(X_test,Y_test)

#prediction
Y_predict=model.predict(X_test)
Y_pred=[]
for label in Y_predict:
  if label<0.5:
    Y_pred.append(0)
  else:
    Y_pred.append(1)
print(Y_pred[:5])
print(Y_test[:5])

#show classification report
print(classification_report(Y_test,Y_pred))

#show confusion matrix
cm=tf.math.confusion_matrix(labels=Y_test,predictions=Y_pred)
plt.figure(figsize=(10,7))
sn.heatmap(cm,annot=True,fmt='d')
plt.xlabel('predicted')
plt.ylabel('Truth')