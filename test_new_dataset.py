
from mclearn import *

# test machine learning models
url = 'dataset1_feature_vector.csv'
dataset = read_dataset(url)
X_train, Y_train = select_features(dataset, 200)

url = 'test_dataset_feature_vector.csv'
test_dataset = read_dataset(url)
X_test, Y_test = select_features(test_dataset, 200)

#model = DecisionTreeClassifier()
model = RandomForestClassifier(n_estimators=100)

for feature_count in range(50,1000,50):
    X_train, Y_train = select_features(dataset, feature_count)
    X_test, Y_test = select_features(test_dataset, feature_count)
    result = test_model(model, X_train, Y_train, X_test, Y_test)
    print("features = %d, accuracy = %f" % (feature_count, result))
