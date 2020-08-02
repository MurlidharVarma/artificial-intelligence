import csv
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    df = pd.read_csv(filename)

    month_arr = ['Jan','Feb', 'Mar','Apr','May','June','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    def transform_month(mon):
        return month_arr.index(mon)

    def transform_visitor_type(typ):
        return 1 if typ == 'Returning_Visitor' else 0
        
    def transform_weekend(wknd):
        return 1 if wknd else 0

    def tansform_revenue(revenue):
        return 1 if revenue else 0

    df['Month'] = df['Month'].apply(transform_month)
    df['VisitorType'] = df['VisitorType'].apply(transform_visitor_type)
    df['Weekend'] = df['Weekend'].apply(transform_weekend)
    df['Revenue'] = df['Revenue'].apply(tansform_revenue)

    evidence = []
    label =[]
    columns = df.columns.tolist()

    for idx in range(0, len(df)):
        evidence_row=[]
        for col in columns:
            if col != "Revenue":
                evidence_row.append(df[col][idx])
        label.append(df['Revenue'][idx])
        evidence.append(evidence_row)

    return (evidence, label)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    postive_total = 0
    negative_total = 0
    sensitivity_count = 0
    specificity_count = 0

    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            postive_total += 1
            if actual == predicted:
                sensitivity_count += 1
        elif actual == 0:
            negative_total += 1
            if actual == predicted:
                specificity_count += 1 

    sensitivity = sensitivity_count/postive_total
    specificity = specificity_count/negative_total
    
    return(sensitivity, specificity)

if __name__ == "__main__":
    main()
