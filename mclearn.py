

import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import json

def cv_models(models, X_train, Y_train):
    # evaluate each model in turn
    seed = 7
    scoring = 'accuracy'
    results = []
    results_dict = {}
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring, n_jobs=-1)
        mean_accuracy = round(100 * cv_results.mean(), 2)
        results.append((name, mean_accuracy))
        results_dict[name] = mean_accuracy
    return results_dict

def save_cv_results(dataset, models, start_feature, end_feature, step_feature, output_filename):
    cvresults={}
    index = 0
    model_names = []
    for model in models:
        model_names.append(model[0])
    # model_names = ['LR', 'KNN', 'DT', 'SVM', 'NB', 'MNB', 'RF']
    cvresults['graph_Xaxis'] = []
    for name in model_names:
        cvresults[name] = []
    for features in range(start_feature,end_feature,step_feature):
        X_train, Y_train = select_features(dataset, features)
        results = cv_models(models, X_train, Y_train)
        print(results)
        cvresults['graph_Xaxis'].append(features)
        for name in model_names:
            cvresults[name].append(results[name])
        index += 1

    ft = open(output_filename, "w")
    ft.write(json.dumps(cvresults))
    ft.close()


def test_model(model, X_train, Y_train, X_test, Y_test):
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)
    # print(accuracy_score(Y_test, predictions) * 100)
    # print(confusion_matrix(Y_test, predictions))
    # print(pandas.crosstab(Y_test, predictions, rownames=['True'], colnames=['Predicted'], margins=True))
    # print(classification_report(Y_test, predictions))
    # print(predictions)
    # print(Y_test)
    # print(X_test)
    result = round(accuracy_score(Y_test, predictions)*100, 2)
    return result


def read_dataset(url):
    try:
        numFeatures = len(open(url, 'r').readline().split(','))
    except FileNotFoundError as e:
        print("Exception type : ", type(e).__name__)
    else:
        attrnames = []
        for i in range(0, numFeatures - 1, 1):
            attrnames.append('String_' + str(i))
        attrnames.append('class')
        dataset = pandas.read_csv(url, names=attrnames)
        print(dataset.shape)
        return dataset
    finally:
        return -1

def select_features(dataset, features_select):
    features_total = dataset.shape[1]
    assert (features_total >= features_select), 'Not enough features to select'
    array = dataset.values
    X = array[:, 0:features_select - 1]
    Y = array[:, features_total - 1]
    return (X, Y)

def split_dataset_features(dataset, features_select):
    features_total = dataset.shape[1]
    assert (features_total >= features_select), 'Not enough features to select'
    array = dataset.values
    X = array[:, 0:features_select - 1]
    Y = array[:, features_total - 1]
    return (X, Y)


if __name__ == "__main__":
#    url = 'globalfeaturevector.txt'
    url = 'mixed.txt'
    dataset = read_dataset(url)
    if dataset == -1:
        print('Cannot read dataset')
        exit()

    # validation_size=0.10
    # seed = 3
    # X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
    # X_train = X
    # Y_train = Y

    # Build Models
    models = []
    models.append(('LR', LogisticRegression()))
    # models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('DT', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('MNB', MultinomialNB()))
    models.append(('SVM', SVC()))
    models.append(('RF', RandomForestClassifier(n_estimators=100)))

    save_cv_results(dataset, models, 0, 1000, 50, "cvgraph.json")

    X_train, Y_train = select_features(dataset, 200)
    url = 'fv20180417-1.txt'
    test_dataset = read_dataset(url)
    X_test, Y_test = select_features(test_dataset, 200)
    model = DecisionTreeClassifier()
    result = test_model(model, X_train, Y_train, X_test, Y_test)
    print("accuracy = ", result)
