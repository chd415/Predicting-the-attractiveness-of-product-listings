import csv
import time
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn import tree
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier

X = []
Y = []
f = np.zeros(9)
enrollment_id = 1
dateformat ='%Y-%m-%dT%H:%M:%S'
startdate=time.strptime('2014-05-31T12:43:20',dateformat)
enddate = startdate



fp1 = open('activity_log.csv')
f1_csv = csv.reader(fp1)
headers1 = next(f1_csv)

for line in f1_csv:
    if line[0] != enrollment_id:
        
        day=(time.mktime(enddate)-time.mktime(startdate))/3600
        if((f[7] == 1)|(day < 0.05)):
            f[8] = 0
        else:
            f[8] = round(day,2)
            
        startdate = time.strptime(line[1],dateformat)
        print(f,line[0]) 
        f[0] = round(f[0]/f[7],6)
        f[1] = round(f[1]/f[7],6)
        f[2] = round(f[2]/f[7],6)
        f[3] = round(f[3]/f[7],6)
        f[4] = round(f[4]/f[7],6)
        f[5] = round(f[5]/f[7],6)
        f[6] = round(f[6]/f[7],6)
        X.append(f)
        enrollment_id = line[0]
        f = np.zeros(9)
    else:
        enddate = time.strptime(line[1],dateformat)
        
    f[7]+=1
    if line[2] == "problem":
        f[0] = f[0] + 1
    if line[2] == "video":
        f[1] = f[1] + 1
    if line[2] == "access":
        f[2] = f[2] + 1
    if line[2] == "wiki":
        f[3] = f[3] + 1
    if line[2] == "discussion":
        f[4] = f[4] + 1
    if line[2] == "navigate":
        f[5] = f[5] + 1
    if line[2] == "page_close":
        f[6] = f[6] + 1
        
X.append(f)
X = np.array(X[1:])
print(X.shape)
fp1.close()

c=[]
d=[]
e=[]
classnum = {}
studentnum = {}
courseid={}
i = 1
fp3 = open('enrollment_list.csv')
f3_csv = csv.reader(fp3)
headers3 = next(f3_csv)
for line in f3_csv:
    if(line[1] in classnum.keys()):
        classnum[line[1]] = classnum[line[1]]+1
    else:
        classnum[line[1]] = 1
        
    if(line[2] in studentnum.keys()):
        studentnum[line[2]] = studentnum[line[2]]+1
    else:
        studentnum[line[2]] = 1
        
    if(line[2] in courseid.keys()):
        e.append(courseid[line[2]])
    else:
        courseid[line[2]] = i
        i=i+1
        e.append(courseid[line[2]])
        
fp3.close()

fp3 = open('enrollment_list.csv')
f3_csv = csv.reader(fp3)
headers3 = next(f3_csv)
for line in f3_csv:
    c.append(classnum[line[1]])
    d.append(studentnum[line[2]])
fp3.close()
print(len(c))
print(len(d))
print(len(e))
X = np.column_stack((X,c))
print('combined')
X = np.column_stack((X,d))
print('combined')
X = np.column_stack((X,e))
print('combined')

fp2 = open('train_label.csv')
f2_csv = csv.reader(fp2)
headers2 = next(f2_csv)
for line in f2_csv:
    Y.append(line[1])
fp2.close()
X_train = X[:72325]
X_test = X[72325:]
print('splitted')
#clf = SVC(probability = True)
#clf = MLPClassifier()
#clf = ExtraTreesClassifier()
clf = GradientBoostingClassifier()
Y_predict = clf.fit(X_train, Y).predict_proba(X_test)
print('predict finished')
with open('predict_result.csv', 'w') as f:
    writer = csv.writer(f)
    print('writing')
    writer.writerows(Y_predict)