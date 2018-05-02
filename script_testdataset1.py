
from mclearn import *

# test machine learning models

dataset1_test_dir = "/home/cloud/Documents/dataset_paper/dataset1_test_results"
ds1_test_results_path = os.path.join(os.getcwd(),"dataset1_test_results")
csv_test_dataset1_fv = os.path.join(ds1_results_path, 'test_dataset1_feature_vector.csv')
test_dataset = read_dataset(csv_test_dataset1_fv)


# train dataset
dataset1_dir = "/home/cloud/Documents/dataset_paper/dataset1"
ds1_results_path = os.path.join(os.getcwd(),"dataset1_results")
csv_dataset1_fv = os.path.join(ds1_results_path, 'dataset1_feature_vector.csv')
train_dataset = read_dataset(csv_dataset1_fv)

for feature_count in range(50,1000,50):
    X_train, Y_train = select_features(dataset, feature_count)
    X_test, Y_test = select_features(test_dataset, feature_count)
    result = test_model(model, X_train, Y_train, X_test, Y_test)
    print("features = %d, accuracy = %f" % (feature_count, result))
