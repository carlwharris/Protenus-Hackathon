from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

# Function to impute missing values
def impute_missing_values(df):
    # Convert 'Snapshot_Date' to datetime for proper sorting
    df['Snapshot_Date'] = pd.to_datetime(df['Snapshot_Date'])

    # Sort the dataframe by 'Opportunity_ID' and 'Snapshot_Date'
    df = df.sort_values(by=['Opportunity_ID', 'Snapshot_Date'], ascending=[True, False])

    # Columns to be imputed
    columns_to_impute = df.columns[df.isna().any()].tolist()

    # Impute missing values
    for col in columns_to_impute:
        # For each Opportunity_ID, fill missing values with the most recent non-null value in the column
        df[col] = df.groupby('Opportunity_ID')[col].transform(lambda group: group.ffill())
    
    # Columns to be imputed (excluding datetime columns)
    columns_to_impute = df.columns[(df.isna().any()) & (df.dtypes != 'datetime64[ns]')]

    # Separate dataframe into numerical and categorical
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns

    # Apply label encoding to categorical columns
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    # Create a copy of the dataframe for imputation
    impute_df = df.copy()

    # Impute missing values using iterative imputation for numerical columns
    for col in columns_to_impute:
        if col in numerical_cols:
            iter_imputer = IterativeImputer()
            impute_df[col] = iter_imputer.fit_transform(impute_df[[col]]).ravel()
        elif col in categorical_cols:
            simple_imputer = SimpleImputer(strategy='most_frequent')
            df[col] = simple_imputer.fit_transform(df[[col]]).ravel()

    # Transfer the imputed values back to the original dataframe
    for col in columns_to_impute:
        df[col].update(impute_df[col])

    # Convert the categorical columns back to their original form
    for col, le in label_encoders.items():
        df[col] = le.inverse_transform(df[col].astype(int))

    return df