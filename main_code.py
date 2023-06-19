# -*- coding: utf-8 -*-
"""My_Cus_segment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vcsPynIhmYC6J-8l4k-C8Jqk7xwLiz-J

**Đề bài**

An automobile company has plans to enter new markets with their existing products (P1, P2, P3, P4 and P5). After intensive market research, they’ve deduced that the behavior of new market is similar to their existing market.

Content In their existing market, the sales team has classified all customers into 4 segments (A, B, C, D ). Then, they performed segmented outreach and communication for different segment of customers. This strategy has work exceptionally well for them.

# **1. Phân tích tập dữ liệu**
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

"""## 1.1 Tổng quan về tập dữ liệu *train*"""

train_dataset = pd.read_csv('Train.csv')

train_dataset.head()

train_dataset.info()

train_dataset.describe()

# Số giá trị null của tập dữ liệu trên từng cột
train_dataset.isnull().sum()

# Trích xuất giá trị có trong mỗi cột
column_names = train_dataset.columns
for i in column_names[1:]:
  if i == 0:
    continue
  print(train_dataset[i].unique())

"""## 1.2. Exploratory Data Analysis + Fill null values + Turn label in to numerical categories"""

# Tạo một tập dữ liệu copy từ train_dataset để tránh thay đổi dữ liệu gốc
train = train_dataset.copy()

"""### 1.2.1 Cột "Gender"
"""

# Số lượng các giá trị trong cột "Gender" theo từng segment
counts = train.groupby(['Gender', 'Segmentation']).size()
print(counts)

# Visualization
counts_df = counts.unstack(level=0)
counts_df.plot(kind='bar')

# Thêm tiêu đề và các nhãn cho biểu đồ
plt.xlabel('Segment')
plt.ylabel('Counts')
plt.legend(['Female', 'Male'])
plt.title(str(counts_df))
plt.show()

"""*Nhận xét: - Trong tất cả các segment, "Female" luôn nhiều hơn "Male"*"""

# Turn label in to numerical categories
train.Gender = pd.Categorical(train.Gender,categories=['Male','Female'],ordered=True).codes

"""### 1.2.2. Cột "Ever_Married"
"""

# Các giá trị trong cột 'Ever_Married'
print("null values:", train.Ever_Married.isnull().sum())
print(train.Ever_Married.value_counts())

# Visualization
counts = train.groupby(['Ever_Married', 'Segmentation']).size()
counts_df = counts.unstack(level=0)
counts_df.plot(kind='bar')

# Thêm nhãn vầ title
plt.xlabel('Segment')
plt.ylabel('Counts')
plt.title(str(counts_df))
plt.show()

"""*Nhận xét: - Nhóm A,B,C chủ yếu là người "ever_married". Trong khi đó, hầu hết người trong nhóm D "not_ever_married"*

**- Fill null values**
"""

# Đếm số lượng các giá trị null trong cột "Ever_Married" của các segment
print(train['Ever_Married'].isna().groupby(train['Segmentation']).sum())

train.loc[train['Segmentation'] == 'D','Ever_Married'] = 'No'
train['Ever_Married'].fillna('Yes',inplace=True)

# Kiểm tra xem còn có giá trị null trong cột "Ever_Married" hay không
print("Number of null values in 'Ever_Married':(after)", train['Ever_Married'].isnull().sum())

# Turn label in to numerical categories
train.Ever_Married=pd.Categorical(train.Ever_Married,categories=['No','Yes'],ordered=True).codes

"""### 1.2.3. Cột "Age"
"""

train['Age'].values

# Looking the distribution of column Age with respect to each segment
a = train[train.Segmentation =='A']["Age"]
b = train[train.Segmentation =='B']["Age"]
c = train[train.Segmentation =='C']["Age"]
d = train[train.Segmentation =='D']["Age"]

plt.figure(figsize=(15,5))

# Creating a boxplot
plt.subplot(1,2,1)
sns.boxplot(x='Segmentation', y='Age', data=train, order = ['A','B','C','D'])
plt.xlabel('Segmentation')
plt.ylabel('Age')
plt.title('Boxplot: Age by Segmentation')
plt.ylim(0, 100)

# Creating a kde plot
plt.subplot(1,2,2)
sns.kdeplot(a,fill = False, label = 'A')
sns.kdeplot(b,fill = False, label = 'B')
sns.kdeplot(c,fill = False, label = 'C')
sns.kdeplot(d,fill = False, label = 'D')
plt.xlabel('Age')
plt.ylabel('Density')
plt.title("Mean\n A: {}\n B: {}\n C: {}\n D: {}".format(round(a.mean(),0),round(b.mean(),0),round(c.mean(),0),round(d.mean(),0)))
plt.legend()

plt.show()

"""Nhận xét:
- Độ tuổi trong segment D thấp nhất nhưng cũng có nhiều outliers tập trung từ 60 đến 90.
- Độ tuổi trong segment A có outliers từ 80 đến 90.
- Độ tuổi trong segment B và C khá tương đồng nhau, phân phối tuổi đồng nhất hơn và không có outliers.

### 1.2.4. Cột "Graduated"
"""

# Các giá trị trong cột 'Graduated'
print("null values:", train.Graduated.isnull().sum())
print(train.Graduated.value_counts())

# Visualization
counts = train.groupby(['Graduated', 'Segmentation']).size()
counts_df = counts.unstack(level=0)
counts_df.plot(kind='bar')

# Thêm nhãn vầ title
plt.xlabel('Segment')
plt.ylabel('Counts')
plt.title(str(counts_df))
plt.show()

"""*Nhận xét: Segment A,B,C phần lớn là người 'Graduated'. Segment D phần lớn là người 'Not Graduated'*

**- Fill null values**
"""

# Đếm số lượng các giá trị null trong cột "Graduated" của các segment
print(train['Graduated'].isna().groupby(train['Segmentation']).sum())

train.loc[train['Segmentation'] == 'D','Graduated'] = 'No'
train.Graduated.fillna('Yes',inplace=True)

# Kiểm tra xem còn có giá trị null trong cột "Graduated" hay không
print("Number of null values in 'Graduated'(after):", train['Graduated'].isnull().sum())

# Turn label in to numerical categories
train.Graduated = pd.Categorical(train.Graduated,categories=['No','Yes'],ordered=True).codes

"""### 1.2.5. Cột "Profession"
"""

# Các giá trị trong cột "Profession"
print("null values:", train.Profession.isnull().sum())
print(train.Profession.value_counts())

value_counts = train.groupby('Segmentation')['Profession'].value_counts()
value_counts.groupby(level=0, group_keys=False).nlargest(len(value_counts))

# Tạo từ điển ánh xạ giữa segment và màu tương ứng
segment_colors = {
    'A': 'blue',
    'B': 'green',
    'C': 'orange',
    'D': 'red'
}

# Tạo subplot với 3 hàng và 3 cột
fig, axs = plt.subplots(3, 3, figsize=(9, 9))

# Lấy danh sách các giá trị trong cột Profession và sắp xếp theo counts
professions = train['Profession'].value_counts().index

# Lấy danh sách các giá trị trong cột Segmentation
segments = train['Segmentation'].unique()

# Duyệt qua từng giá trị trong cột Profession và vẽ plot tương ứng
for i, profession in enumerate(professions):
    row = i // 3
    col = i % 3
    ax = axs[row, col]

    # Lọc dữ liệu theo giá trị của Profession
    data = train[train['Profession'] == profession]

    # Vẽ biểu đồ cột trong plot hiện tại
    for j, segment in enumerate(segments):
        segment_data = data[data['Segmentation'] == segment]
        ax.bar(segment, segment_data.shape[0], color=segment_colors[segment])

    # Đặt tiêu đề cho plot
    ax.set_title(f'{profession}')

# Cân chỉnh và hiển thị subplot
plt.tight_layout()
plt.show()

"""*Nhận xét: Nhóm A, B, C nhiều nhất là Artist, D nhiều nhất là Healthcare*

**- Fill null values**
"""

# Đếm số lượng các giá trị null trong cột "Profession" của các segment
print(train['Profession'].isna().groupby(train['Segmentation']).sum())

train.loc[train['Segmentation'] == 'D','Profession'] = 'Healthcare'
train.Profession.fillna('Artist',inplace=True)

# Kiểm tra xem còn có giá trị null trong cột "Profession" hay không
print("Number of null values in 'Profession'(after):", train['Profession'].isnull().sum())
# Các giá trị trong cột "Profession"
print(train.Profession.value_counts())

# Turn label in to numerical categories
train.Profession=pd.Categorical(train.Profession,categories=['Homemaker', 'Artist', 'Healthcare', 'Entertainment', 'Doctor', 'Lawyer', 'Executive', 'Marketing', 'Engineer'],ordered=True).codes

"""### 1.2.6 Cột "Speding_Score"
"""

# Đếm số lượng các giá trị null trong cột "Spending_Score" của các segment
count_ss = train.groupby(["Segmentation"])["Spending_Score"].value_counts().unstack()
print(count_ss)

# Visualize
count_ss.plot(kind = 'bar')
plt.title(str(count_ss))
plt.show()

# Turn label in to numerical categories
train.Spending_Score=pd.Categorical(train.Spending_Score,categories=['Low','Average','High'],ordered=True).codes

"""### 1.2.7. Cột "Work_Experience"
"""

# Các giá trị trong cột "Work_Experience"
print("null values:", train.Work_Experience.isnull().sum())
print(train.Work_Experience.value_counts())

# Looking the distribution of column Work_Experience w.r.t to each segment
a = train[train.Segmentation =='A']["Work_Experience"]
b = train[train.Segmentation =='B']["Work_Experience"]
c = train[train.Segmentation =='C']["Work_Experience"]
d = train[train.Segmentation =='D']["Work_Experience"]

plt.figure(figsize=(15,5))

plt.subplot(1,2,1)
sns.boxplot(data = train, x = "Segmentation", y="Work_Experience", order = ['A','B','C','D'])
plt.title('Boxplot')

plt.subplot(1,2,2)
sns.kdeplot(a,fill = False, label = 'A')
sns.kdeplot(b,fill = False, label = 'B')
sns.kdeplot(c,fill = False, label = 'C')
sns.kdeplot(d,fill = False, label = 'D')
plt.xlabel('Work Experience')
plt.ylabel('Density')
plt.title("Mean\n A: {}\n B: {}\n C: {}\n D: {}".format(round(a.mean(),0),round(b.mean(),0),round(c.mean(),0),round(d.mean(),0)))

plt.show()

# Đếm số lượng các giá trị null trong cột "Work_Experience" của các segment
print(train['Work_Experience'].isna().groupby(train['Segmentation']).sum())

"""*Cột này sẽ được bỏ đi vì dữ liệu sẽ không giúp ích nhiều*"""

### 1.3.8. Cột "Family_Size"

# Các giá trị trong cột "Family_Size"
print("null values:", train.Family_Size.isnull().sum())
print(train.Family_Size.value_counts())

# Looking the distribution of column Family Size w.r.t to each segment
a = train[train.Segmentation =='A']["Family_Size"]
b = train[train.Segmentation =='B']["Family_Size"]
c = train[train.Segmentation =='C']["Family_Size"]
d = train[train.Segmentation =='D']["Family_Size"]

plt.figure(figsize=(15,5))

plt.subplot(1,2,1)
sns.boxplot(data = train, x = "Segmentation", y="Family_Size", order = ['A','B','C','D'])
plt.title('Boxplot')

plt.subplot(1,2,2)
sns.kdeplot(a, fill = False, label = 'A')
sns.kdeplot(b, fill = False, label = 'B')
sns.kdeplot(c, fill = False, label = 'C')
sns.kdeplot(d, fill = False, label = 'D')
plt.xlabel('Family Size')
plt.ylabel('Density')
plt.title("Mean\n A: {}\n B: {}\n C: {}\n D: {}".format(round(a.mean(),0),round(b.mean(),0),round(c.mean(),0),round(d.mean(),0)))
plt.legend()

plt.show()

"""*Nhận xét: 'Family_Size' của B,C,D khá tương đồng nhau, trong khi của A thấp hơn.*

**- Fill null values**
"""

# Đếm số lượng các giá trị null trong cột "Family_Size" của các segment
print(train['Family_Size'].isna().groupby(train['Segmentation']).sum())

train.Family_Size.fillna(2,inplace=True)

# Kiểm tra xem còn có giá trị null trong cột "Family_Size" hay không
print("null values:", train.Family_Size.isnull().sum())
# Các giá trị trong cột "Family_Size"
print(train.Family_Size.value_counts())

"""### 1.2.8. Cột "Var_1"
"""

# Các giá trị trong cột "Var_1"
print("null values:", train.Var_1.isnull().sum())
print(train.Var_1.value_counts())

# Counting Var_1 in each segment
ax1 = train.groupby(["Segmentation"])["Var_1"].value_counts().unstack().round(3)

# Percentage of category of Var_1 in each segment
ax2 = train.pivot_table(columns='Var_1',index='Segmentation',values='ID',aggfunc='count')
ax2 = ax2.div(ax2.sum(axis=1), axis = 0).round(2)

#count plot
fig, ax = plt.subplots(1,2)
ax1.plot(kind="bar",ax = ax[0],figsize = (15,4))
ax[0].set_xticklabels(labels = ['A','B','C','D'],rotation = 0)
ax[0].set_title(str(ax1))

#stacked bars
ax2.plot(kind="bar",stacked = True,ax = ax[1],figsize = (15,4))
ax[1].set_xticklabels(labels = ['A','B','C','D'],rotation = 0)
ax[1].set_title(str(ax2))
plt.show()

"""*Nhận xét: Cat_6 chiếm phần lớn trong tất cả các segment*

**- Chuyển tất cả các giá trị null thành Cat_6**
"""

train.Var_1.fillna('Cat_6',inplace=True)

train.Var_1 = pd.Categorical(train.Var_1,categories=['Cat_1', 'Cat_2', 'Cat_3', 'Cat_4', 'Cat_5', 'Cat_6', 'Cat_7'],ordered=True).codes

"""## 1.3 Feature Engineering"""

# Chuyển cột 'Segmentation' sang numerical
train.Segmentation = pd.Categorical (train.Segmentation, categories = ['A', 'B', 'C', 'D'], ordered = True).codes

# Drop cột 'ID'
train.drop('ID', axis = 1, inplace = True)

# bảng correlation giữa các cột vs nhau
cor = train.corr(method='pearson')

# select features that have high absolute correlation with output.
fig, ax = plt.subplots(figsize=(11,11))         # Sample figsize in inches
sns.heatmap(
    cor, #dataset
    vmin=-1, vmax=1, #values to anchor the heatmap
    center=0, #value để center, look at the color bar
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True, #each cell is square-shaped
    ax=ax,
    annot=True #để mỗi cell có text
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);

# Corr của work experience, var 1, gender < 0,1 -> bỏ
train = train.drop ('Work_Experience', axis =1)
train = train.drop ('Var_1', axis = 1)
train = train.drop ('Gender', axis = 1)

# Xem dữ liệu trong 'train' sau khi chuyển đổi sang numerical
train

"""**=> Từ phần 1, ta có một bộ dữ liệu numerical dựa trên 'train_dataset', ta sẽ gán dữ liệu này là 'data'**"""

data = train.copy()

data.info()

"""# **2. Phân loại dữ liệu bằng các mô hình học máy**

## 2.1. Thử các mô hình học máy

Dùng các model: *Softmax Regression, KNeighborsClassifiers, LGMCLassifier, DecisionTreeClassifier, RandomForestClassifier, SupportVectorMachineClassifier, NaiveBayesCLassifier* để phân loại dữ liệu train. Sau đó chọn mô hình tốt nhất để tối ưu.
"""

from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn.metrics import accuracy_score

from lightgbm  import LGBMClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble    import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB

"""Chia dữ liệu 'data' thành X_train, y_train, X_val, y_val"""

X = data.values[:,:6]   # X.shape = (8068,8)
y = data.values[:,6]    # Y.shape = (8068,)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.2, random_state = 42)

print('X_train.shape:', X_train.shape)
print('y_train.shape:', y_train.shape)
print('X_val.shape:', X_val.shape)
print('y_val.shape:', y_val.shape)

# k-fold
num_folds = 10
seed = 42
scoring = 'accuracy'

models = []
models.append(('LR', LogisticRegression(multi_class = 'multinomial', max_iter = 10000)))
models.append(('KNN', KNeighborsClassifier()))
models.append(('LGB', LGBMClassifier()))
models.append(('Decision tree', DecisionTreeClassifier(max_depth = 10)))
models.append(('Random Forest', RandomForestClassifier()))
models.append(('SVC', SVC(decision_function_shape = 'ovo')))
models.append(('Naive Bayes', GaussianNB()))

# evaluate each model in turn
results = []
names = []
for name, model in models:
 kfold = model_selection.KFold(n_splits=10, shuffle = True, random_state=seed)
 cv_results = model_selection.cross_val_score(model, X, y, cv=kfold, scoring=scoring)
 results.append(cv_results)
 names.append(name)
 msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
 print(msg)

fig = plt.figure(figsize=(15, 15))
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import *

pipelines = []
pipelines.append(('ScaledLR', Pipeline([('Scaler', StandardScaler()),('LR',LogisticRegression(multi_class = 'multinomial', max_iter=1000))])))
pipelines.append(('ScaledKNN', Pipeline([('Scaler', StandardScaler()),('KNN',KNeighborsClassifier())])))
pipelines.append(('ScaledCART', Pipeline([('Scaler', StandardScaler()),('Decision Tree',DecisionTreeClassifier())])))
pipelines.append(('ScaledLGB', Pipeline([('Scaler', StandardScaler()),('LGB', LGBMClassifier())])))
pipelines.append(('ScaledKNN', Pipeline([('Scaler', StandardScaler()),('Random Forest', RandomForestClassifier())])))
pipelines.append(('ScaledSVC', Pipeline([('Scaler', StandardScaler()),('SVC', SVC(decision_function_shape='ovo'))])))
pipelines.append(('ScaledNaive', Pipeline([('Scaler', StandardScaler()),('Naive Bayes', GaussianNB())])))


results = []
names = []
for name, model in pipelines:
  kfold = KFold(n_splits=num_folds, shuffle = True, random_state=seed)
  cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
  results.append(cv_results)
  names.append(name)
  msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
  print(msg)

# Compare Algorithms đã chuẩn hóa
fig = plt.figure(figsize=(12, 12))
fig.suptitle('Scaled Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

"""#### => Ở cả 'Not_Scaled_Data' và 'Scaled_Data', LGBMClassifier đều cho kết quả tốt nhất. Do đó, ta sẽ chọn tối ưu hóa mô hình này

## 2.2. Tối ưu hóa LGBMClassifier
"""

from sklearn.model_selection import RandomizedSearchCV

model = LGBMClassifier()
parameters = {'learning_rate': [0.01], 'n_estimators': [8, 24],
    'num_leaves':[20,40,60,80,100], 'min_child_samples':[5,10,15],'max_depth':[-1,5,10,20],
             'learning_rate':[0.05,0.1,0.2],'reg_alpha':[0,0.01,0.03], 'colsample_bytree': [0.65, 0.75, 0.8],}
clf = RandomizedSearchCV(model, parameters, scoring = 'accuracy', n_iter=100)
clf.fit(X = X_train, y = y_train)
print(clf.best_params_)
predicted = clf.predict(X_val)
print('Classification of the result is:')
print(accuracy_score(y_val, predicted))

"""=> Tham số tốt nhất là: *{'reg_alpha': 0.03, 'num_leaves': 20, 'n_estimators': 24, 'min_child_samples': 10, 'max_depth': 10, 'learning_rate': 0.1, 'colsample_bytree': 0.65}*"""

best_lgbm = LGBMClassifier(reg_alpha=0.03, num_leaves=20, n_estimators=24, min_child_samples=10, max_depth=10, learning_rate=0.1, colsample_bytree=0.65)
best_lgbm.fit(X_train, y_train)

from sklearn.metrics import *

predictions = best_lgbm.predict(X_val)
print (classification_report(y_val, predictions))

cm = confusion_matrix(y_val, predictions)
print(cm)

# Visualize bằng seaborn
plt.figure(figsize=(9,9))
sns.heatmap(cm, annot=True, fmt="n", linewidths=.5, square = True, cmap = 'bone_r');
plt.ylabel('Actual label');
plt.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {0}'.format(accuracy_score(y_val, predicted))
plt.title(all_sample_title, size = 15);

import lightgbm as lgb
from IPython.display import Image
import pydotplus

# Tạo đồ thị cây quyết định
graph = lgb.create_tree_digraph(best_lgbm, tree_index=3, name='Tree3')

# Chuyển đổi đồ thị thành hình ảnh
image = pydotplus.graph_from_dot_data(graph.source).create_png()

# Hiển thị hình ảnh
Image(image)

"""# **3. Phân loại dữ liệu bằng mô hình Deep Learning**


"""

from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras.layers import Dropout

# Mã hóa nhãn y
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_val_encoded = label_encoder.transform(y_val)

# Chuyển đổi nhãn y sang dạng one-hot
num_classes = len(label_encoder.classes_)
y_train_onehot = np_utils.to_categorical(y_train_encoded, num_classes)
y_val_onehot = np_utils.to_categorical(y_val_encoded, num_classes)

# Xây dựng kiến trúc mô hình
model_DL = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(6,)),
    Dropout(0.5),  # Thêm dropout với tỷ lệ loại bỏ 50%
    keras.layers.Dense(64, activation='relu'),
    Dropout(0.5),  # Thêm dropout với tỷ lệ loại bỏ 50%
    keras.layers.Dense(num_classes, activation='softmax')
])

# Compile mô hình
model_DL.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
model_DL.fit(X_train, y_train_onehot, epochs=20, batch_size=32, validation_data=(X_val, y_val_onehot))

# Đánh giá mô hình
test_loss, test_acc = model_DL.evaluate(X_val, y_val_onehot)
print('Test accuracy:', test_acc)

"""# **4. Sử dụng mô hình để dự đoán trên tập test**

*Import tập dữ liệu test*
"""

Test = pd.read_csv('Test.csv')

Test.isnull().sum()

# Biến đổi dữ liệu tập test như tập train
Test.Gender = pd.Categorical(Test.Gender,categories=['Male','Female'],ordered=True).codes
Test.loc[Test['Segmentation'] == 'D','Ever_Married'] = 'No'
Test['Ever_Married'].fillna('Yes',inplace=True)
Test.Ever_Married=pd.Categorical(Test.Ever_Married,categories=['No','Yes'],ordered=True).codes
Test.loc[Test['Segmentation'] == 'D','Graduated'] = 'No'
Test.Graduated.fillna('Yes',inplace=True)
Test.Graduated = pd.Categorical(Test.Graduated,categories=['No','Yes'],ordered=True).codes
Test.loc[Test['Segmentation'] == 'D','Profession'] = 'Healthcare'
Test.Profession.fillna('Artist',inplace=True)
Test.Profession=pd.Categorical(Test.Profession,categories=['Homemaker', 'Artist', 'Healthcare', 'Entertainment', 'Doctor', 'Lawyer', 'Executive', 'Marketing', 'Engineer'],ordered=True).codes
Test.Spending_Score=pd.Categorical(Test.Spending_Score,categories=['Low','Average','High'],ordered=True).codes
Test.Family_Size.fillna(2,inplace=True)
Test.Var_1.fillna('Cat_6',inplace=True)
Test.Var_1 = pd.Categorical(Test.Var_1,categories=['Cat_1', 'Cat_2', 'Cat_3', 'Cat_4', 'Cat_5', 'Cat_6', 'Cat_7'],ordered=True).codes
Test.Segmentation = pd.Categorical (Test.Segmentation, categories = ['A', 'B', 'C', 'D'], ordered = True).codes
Test = Test.drop ('ID', axis =1)
Test = Test.drop ('Work_Experience', axis =1)
Test = Test.drop ('Var_1', axis = 1)
Test = Test.drop ('Gender', axis = 1)
Test

X_test = Test.values[:,:6]
y_test = Test.values[:,6]
print(X_test.shape)
print(y_test.shape)

"""## 4.1. Sử dụng model LGBMClassifier đã tối ưu"""

y_pred = best_lgbm.predict(X_test)

from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

"""## 4.2. Sử dụng DeepLearning"""

y_test_encoded = label_encoder.transform(y_test)
y_test_onehot = np_utils.to_categorical(y_test_encoded, num_classes)
test_loss, test_acc = model_DL.evaluate(X_test, y_test_onehot)
print('Test accuracy:', test_acc)