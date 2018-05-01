
from mclearn import *

url = 'dataset2_feature_vector.csv'
dataset = read_dataset(url)
X_train, Y_train = select_features(dataset, 200)

url = 'fv20180417-1.txt'
test_dataset = read_dataset(url)
X_test, Y_test = select_features(test_dataset, 200)

model = DecisionTreeClassifier()
result = test_model(model, X_train, Y_train, X_test, Y_test)
print("accuracy = ", result)
