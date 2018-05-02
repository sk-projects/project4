from mclearn import *
from fileinfo import FileList

dataset1_dir = "/home/cloud/Documents/dataset_paper/dataset1"
ds1_results_path = os.path.join(os.getcwd(),"dataset1_results")
objfile_benign = os.path.join(ds1_results_path, 'benign_dataset1.pkl')
objfile_malware = os.path.join(ds1_results_path, 'malware_dataset1.pkl')
objfile_dataset1 = os.path.join(ds1_results_path, 'dataset1.pkl')
csv_dataset1_fv = os.path.join(ds1_results_path, 'dataset1_feature_vector.csv')
file_fl_dataset1 = os.path.join(ds1_results_path, 'dataset1_feature_list.txt')

dataset1_test_dir = "/home/cloud/Documents/dataset_paper/dataset1_test_results"
ds1_test_results_path = os.path.join(os.getcwd(),"dataset1_test_results")
csv_test_dataset1_fv = os.path.join(ds1_results_path, 'test_dataset1_feature_vector.csv')
test_dataset = read_dataset(csv_test_dataset1_fv)

# train dataset
dataset1_dir = "/home/cloud/Documents/dataset_paper/dataset1"
ds1_results_path = os.path.join(os.getcwd(),"dataset1_results")
csv_dataset1_fv = os.path.join(ds1_results_path, 'dataset1_feature_vector.csv')
train_dataset = read_dataset(csv_dataset1_fv)

print("Testing performance on unseen data")
models = initialize_models()
save_test_results(train_dataset, test_dataset, models, 50, 1001, 50, json_dataset1_test_results)
save_test_cm_results(train_dataset, test_dataset, models, start_feature, end_feature, step_feature, output_filename)
plot_graph('Test Results for Unseen Dataset', 'Number of Features', 'Accuracy', json_dataset1_test_results, png_dataset1_test_results)

from FormatResult import *
write_cv_results_to_excel(json_dataset1_test_results, os.path.join(result_test_directory,'dataset1_test_result.xlsx'))


