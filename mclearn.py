
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

def crossvalidate_models(models, X_train, Y_train):
    # evaluate each model in turn
    seed = 7
    scoring = 'accuracy'
    results = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring, n_jobs=-1)
        results.append((name,cv_results.mean()*100))
    return results


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
    result = accuracy_score(Y_test, predictions)*100
    return result

def read_dataset(url):
    numTopFeatures = 200
    numFeatures = 200
    attrnames = []
    for i in range(0, numFeatures - 1, 1):
        attrnames.append('String_' + str(i))
    attrnames.append('class')
    dataset = pandas.read_csv(url, names=attrnames)
    print(dataset.shape)
    array = dataset.values
    X = array[:, 0:numTopFeatures - 1]
    Y = array[:, numFeatures - 1]
    print(X)
    print(Y)
    return (X,Y)

if __name__ == "__main__":


    url = 'globalfeaturevector.txt'
    X,Y = read_dataset(url)

    url = 'fv20180417-1.txt'
    X_test,Y_test = read_dataset(url)

    # Build Models
    models = []
    models.append(('LR', LogisticRegression()))
    # models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
#    models.append(('DT', DecisionTreeClassifier()))
#    models.append(('NB', GaussianNB()))
#    models.append(('MNB', MultinomialNB()))
#    models.append(('SVM', SVC()))
#    results = crossvalidate_models(models, X, Y)
#    print(results)

    model = DecisionTreeClassifier()
    result = test_model(model, X, Y, X_test, Y_test)
    print("accuracy = ", result)