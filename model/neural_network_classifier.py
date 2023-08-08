
#%% Package Imports

import os
import pickle

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from itertools import cycle
from scipy.stats import randint
from collections import Counter

from sklearn.neural_network import MLPClassifier
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

from sklearn.pipeline import (
    Pipeline,
    FeatureUnion
)
from sklearn.preprocessing import (
    LabelBinarizer,
    StandardScaler,
    OneHotEncoder,
    OrdinalEncoder
)
from sklearn.base import (
    BaseEstimator,
    TransformerMixin
)
from sklearn.metrics import (
    auc,
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
    RocCurveDisplay,
    PrecisionRecallDisplay,
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    ConfusionMatrixDisplay,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import (
    cross_validate,
    cross_val_score
)

#%% Set Output Environment

root = '/Users/edf/repos/carb_elec/model/saved/'
os.chdir(root)

#%% Class Definitions

class DataFrameSelector(BaseEstimator, TransformerMixin):
    '''Custom class to support the pipeline filtering of input pandas dataframes
    on the basis of attribute field name lists'''

    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y = None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values
    def feature_names_in_(self, X):
        return X.columns.to_list()

#%% Function Definitions

def ImportRaw(sector):
    '''Function to import pre-processed buildind permit training data from
    local postgres database'''

    # Extract Database Connection Parameters from Environment
    host = os.getenv('PGHOST')
    user = os.getenv('PGUSER')
    password = os.getenv('PGPASS')
    port = os.getenv('PGPORT')
    db = 'carb'

    # Establish DB Connection
    db_con_string = 'postgresql://' + user + '@' + host + ':' + port + '/' + db
    db_con = sql.create_engine(db_con_string)

    # Switch on Sector
    if sector == 'single_family':
        query = ''' SELECT * FROM la100.sf_training_full;'''
    elif sector == 'multi_family':
        query = '''SELECT * FROM la100.mf_training_full;'''
    else:
        raise Exception("Sector must be either 'single-family' or multi_family'")

    raw = pd.read_sql(query, db_con)
    raw.set_index('rowid', drop = True, inplace = True)

    return raw

#%% Compute ROC Statistics

def ROCStats(y_test_binary, predict_test_score, n_classes):

    fpr, tpr, roc_auc = dict(), dict(), dict()
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test_binary.ravel(), predict_test_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_binary[:, i], predict_test_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    fpr_grid = np.linspace(0.0, 1.0, 1000)

    # Interpolate all ROC curves at these points
    mean_tpr = np.zeros_like(fpr_grid)

    for i in range(n_classes):
        mean_tpr += np.interp(fpr_grid, fpr[i], tpr[i])  # linear interpolation

    # Average it and compute AUC
    mean_tpr /= n_classes

    fpr["macro"] = fpr_grid
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

    return tpr, fpr, roc_auc

#%% Compute Precision and Recall Statistics

def PrecisionRecallStats(y_test_binary, predict_test_score, n_classes):

    precision = dict()
    recall = dict()
    average_precision = dict()

    for i in range(n_classes):
        precision[i], recall[i], _ = precision_recall_curve(y_test_binary[:, i], predict_test_score[:, i])
        average_precision[i] = average_precision_score(y_test_binary[:, i], predict_test_score[:, i])

    precision["micro"], recall["micro"], _ = precision_recall_curve(
        y_test_binary.ravel(), predict_test_score.ravel()
    )
    average_precision["micro"] = average_precision_score(y_test_binary, predict_test_score, average="micro")

    return precision, recall, average_precision

#%% Plot Micro and Macro ROC Curves

def PlotROCAverages(tpr, fpr, roc_auc):

    fig, ax = plt.subplots(figsize=(9, 9))

    x_lin = np.linspace(0,1,100)
    y_lin = np.linspace(0,1,100)

    ax.plot(x_lin, y_lin, linestyle = '--', color = 'k', linewidth = 1.5)

    ax.plot(
        fpr["micro"],
        tpr["micro"],
        label=f"micro-average ROC curve (AUC = {roc_auc['micro']:.2f})",
        color="deeppink",
        linestyle=":",
        linewidth=4,
    )

    ax.plot(
        fpr["macro"],
        tpr["macro"],
        label=f"macro-average ROC curve (AUC = {roc_auc['macro']:.2f})",
        color="navy",
        linestyle=":",
        linewidth=4,
    )

    plt.grid(True)
    plt.axis("square")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Extension of Receiver Operating Characteristic\nto Micro & Macro multiclass")
    plt.legend()
    plt.show()

    return fig, ax

#%% Plot One-vs-Rest ROC Curves

def PlotROCOneVsRest(y_test_binary, predict_test_score, class_names, n_classes):

    fig, ax = plt.subplots(figsize=(9, 9))

    colors = sns.color_palette(None, n_classes)

    for class_id, color in zip(range(n_classes), colors):
        RocCurveDisplay.from_predictions(
            y_test_binary[:, class_id],
            predict_test_score[:, class_id],
            name = f"ROC curve for {class_names[class_id]}",
            color = color,
            ax = ax,
            plot_chance_level = (class_id == 0),
        )

    plt.grid(True)
    plt.axis("square")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Extension of Receiver Operating Characteristic\nto One-vs-Rest multiclass")
    plt.legend()
    plt.show()

    return fig, ax

#%% Plot Micro-Average Precision-Recall Curve

def PlotPRMicroAverages(recall, precision, average_precision, y_test):

    fig, ax = plt.subplots(1, 1, figsize=(9, 9))

    display = PrecisionRecallDisplay(
        recall=recall["micro"],
        precision=precision["micro"],
        average_precision=average_precision["micro"],
        prevalence_pos_label=Counter(y_test.ravel())[1] / y_test.size,
    )

    display.plot(plot_chance_level = True, ax = ax)
    ax.set_title("Precision-Recall Curve\n Micro-averaged Over All Classes")
    ax.legend(loc = 'best')
    ax.grid(True)

    return fig, ax

#%% Plot Class Level Precision-Recall Curves

def PlotPRClassLevel(recall, precision, average_precision, n_classes):

    fig, ax = plt.subplots(figsize=(9, 9))

    f_scores = np.linspace(0.2, 0.8, num=4)
    lines, labels = [], []
    for f_score in f_scores:
        x = np.linspace(0.01, 1)
        y = f_score * x / (2 * x - f_score)
        (l,) = plt.plot(x[y >= 0], y[y >= 0], color="gray", alpha=0.2)
        plt.annotate("f1={0:0.1f}".format(f_score), xy=(0.9, y[45] + 0.02))

    display = PrecisionRecallDisplay(
        recall=recall["micro"],
        precision=precision["micro"],
        average_precision=average_precision["micro"],
    )
    display.plot(ax=ax, name="Micro-average precision-recall", color="gold")

    for i, color in zip(range(n_classes), colors):
        display = PrecisionRecallDisplay(
            recall=recall[i],
            precision=precision[i],
            average_precision=average_precision[i],
        )
        display.plot(ax=ax, name=f"Precision-recall for class {i}", color=color)

    handles, labels = display.ax_.get_legend_handles_labels()
    handles.extend([l])
    labels.extend(["iso-f1 curves"])
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.legend(handles=handles, labels=labels, bbox_to_anchor=(1.05, 0.8))
    ax.set_title("Precision-Recall Curve\n for Each Individual Class")

    plt.show()

    return fig, ax

#%% Plot Within-Class Count Normalized Confusion Matrix

def PlotWithinClassNormalizedConfusionMatrix(mlp_clf, X_test, y_test, class_names):

    fig, ax = plt.subplots(1,1,figsize=(15,11))

    cat_norm = ConfusionMatrixDisplay.from_estimator(
        mlp_clf,
        X_test,
        y_test,
        display_labels=class_names,
        cmap=plt.cm.Blues,
        normalize= 'true',
        ax = ax
    )

    cat_norm.ax_.set_title('Confusion Matrix\nWithin-Class, Count Normalized')

    return fig, ax

#%% Plot Across Class Count Normalized Confusion Matrix

def PlotAcrossClassCountNormalizedConfusionnMatrix(mlp_clf, X_test, y_test, class_names):

    fig, ax = plt.subplots(1,1,figsize=(15,11))

    all_norm = ConfusionMatrixDisplay.from_estimator(
        mlp_clf,
        X_test,
        y_test,
        display_labels=class_names,
        cmap=plt.cm.Reds,
        normalize= 'all',
        ax = ax
    )

    all_norm.ax_.set_title('Confusion Matrix\nAll-Class, Count Normalized')

    return fig, ax

#%% Extract Training Data

sector = 'single_family'
data = ImportRaw(sector)

#%% Get Training Feature Types

output_attrib = ['panel_size_existing']

passthrough_attribs = [ 'slopepct',
                        'peopcolorpct',
                        'lowincpct',
                        'unemppct',
                        'lingisopct',
                        'lesshspct',
                        'under5pct',
                        'over64pct',
                        'lifeexppct',
                        'renterhouseholdspct',
                        'elecheatinghouseholdspct']

fill_attribs = ['HeatingTypeorSystemStndCode',
                'AirConditioningTypeorSystemStndCode']

num_attribs = list(data.select_dtypes(include=[np.number]).columns)
for val in passthrough_attribs:
    if (val in num_attribs):
        num_attribs.remove(val)

cat_attribs = list(data.select_dtypes(include=[object]).columns)
for val in fill_attribs:
    if (val in cat_attribs):
        cat_attribs.remove(val)

num_attribs.remove(output_attrib[0])

#%% Split Inputs from Outputs

inputs = data[passthrough_attribs + fill_attribs + num_attribs + cat_attribs]
outputs = data[output_attrib]

#%% Construct Training Feature Pipeline

passthrough_pipeline = Pipeline([
    ('selector', DataFrameSelector(passthrough_attribs)),
    ('passthrough_imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'median')),
])

fill_pipeline = Pipeline([
    ('selector', DataFrameSelector(fill_attribs)),
    ('fill_imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'constant',
        fill_value = 'NA')),
    ('one_hot_encoder', OneHotEncoder(sparse_output = False))
])

numeric_pipeline = Pipeline([
    ('selector', DataFrameSelector(num_attribs)),
    ('imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'median')),
    ('std_scaler', StandardScaler()),
])

categorical_pipeline = Pipeline([
    ('selector', DataFrameSelector(cat_attribs)),
    ('imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'most_frequent')),
    ('one_hot_encoder', OneHotEncoder(sparse_output = False)),
])

input_pipeline = FeatureUnion(transformer_list = [
    ('passthrough_pipeline', passthrough_pipeline),
    ('fill_pipeline', fill_pipeline),
    ('numeric_pipeline', numeric_pipeline),
    ('categorical_pipeline', categorical_pipeline),
])

X = input_pipeline.fit_transform(inputs)

#%% Construct Ouput Feature Pipleine

output_pipeline = Pipeline([
    ('selector', DataFrameSelector(output_attrib)),
    ('imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'most_frequent')),
    ('ordinal_encoder', OrdinalEncoder())
])

y = output_pipeline.fit_transform(outputs)

#%% Training Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=69,
    stratify = y)

y_train = y_train.ravel()
y_test = y_test.ravel()

#%% Fit Model and Save Weights

# Specify Hidden Layer Counts
hlc = 3

# Specify Hidden Layer Node Counts
hlnc = X_train.shape[1]

# Specify Hidden Layers
hl = np.repeat(hlnc, hlc)

# Set Model Parameters
mlp_clf = MLPClassifier(
    hidden_layer_sizes = hl,
    activation = 'relu',
    solver = 'adam',
    max_iter = 500,
    verbose = True,
    warm_start = True)

mlp_clf.fit(X_train, y_train)

# Save CV Object
filename = 'mlp_clf.pkl'
pickle.dump(mlp_clf, open(filename, 'wb'))

#%% Cross Validate

scoring = ['precision_macro', 'recall_macro']

mlp_clf_cv = MLPClassifier(
    hidden_layer_sizes = hl,
    activation = 'relu',
    solver = 'adam',
    max_iter = 500,
    verbose = True)

mlp_clf_cv_results = cross_validate(
    mlp_clf_cv,
    X_train,
    y_train,
    cv = 5,
    scoring = scoring,
    return_estimator = True)

# Save CV Results Object
filename = 'mlp_clf_cv_results.pkl'
pickle.dump(mlp_clf_cv_results, open(filename, 'wb'))

#%% Predict and Evaluate Accuracy on Test Set

predict_train = mlp_clf.predict(X_train)
predict_test = mlp_clf.predict(X_test)
predict_test_score = mlp_clf.predict_proba(X_test)

#%% Print Accuracy, Confusion Matrix, and Classification Report

accuracy = accuracy_score(y_test, predict_test)
confusion_mat = confusion_matrix(y_train, predict_train)
clf_report = classification_report(y_train, predict_train)

print(accuracy)
print(confusion_mat)
print(clf_report)

#%% Generate Class Names and Counts

class_names = list(np.sort(outputs[output_attrib[0]].unique()))[:-1]
n_classes = len(np.unique(y_train))

#%% Generate Binary Label Representation for Test Data

y_test_binary = LabelBinarizer().fit(y_test).transform(y_test)

#%% Compute ROC and PR Stats

tpr, fpr, roc_auc = ROCStats(
    y_test_binary, predict_test_score, n_classes)
precision, recall, average_precision = PrecisionRecallStats(
    y_test_binary, predict_test_score, n_classes)

#%% Generate Diagnostic Plots

fig1, ax1 = PlotROCAverages(
    tpr, fpr, roc_auc)
fig2, ax2 = PlotROCOneVsRest(
    y_test_binary, predict_test_score, class_names, n_classes)
fig3, ax3 = PlotPRMicroAverages(
    recall, precision, average_precision, y_test)
fig4, ax4 = PlotPRClassLevel(
    recall, precision, average_precision, n_classes)
fig5, ax5 = PlotWithinClassNormalizedConfusionMatrix(
    mlp_clf, X_test, y_test, class_names)
fig6, ax6 = PlotAcrossClassCountNormalizedConfusionMatrix(
    mlp_clf, X_test, y_test, class_names)
