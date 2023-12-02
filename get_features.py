import pandas as pd

months_df = pd.read_csv('Protenus Sales Training Data.csv')

def get_q_num(df):
    quarter = df['Quarter']

    # Drop the Qs from each entry and convert to int
    quarter = quarter.str.replace('Q', '').astype(int)
    df['quarter_num'] = quarter

    return df

# How many Qs has the deal been activive for
def get_active_days(df):
    df['Snapshot_Date'] = pd.to_datetime(df['Snapshot_Date'])
    df['Opportunity_Created_Date'] = pd.to_datetime(df['Opportunity_Created_Date'])
    df['active_days'] = df['Snapshot_Date'] - df['Opportunity_Created_Date']
    df['active_days'] = df['active_days'].dt.days
    return df

def get_mos_stages(df):
    stages = ['Stage 3 - Pricing', 'Stage 2 - Scoping', 'Stage 1 - Evaluating', 'Stage 4 - Verbal / VOC',
          'Closed Lost', 'Stage 5 - Contracting', 'Closed Won', 'Stage 0 - Prospecting']

    # Iterate through each stage and create a new column for each stage
    for stage in stages:
        column_name = f'Stage_Sum_{stage.replace(" ", "_").replace("/", "_").replace("-", "_")}'
        months_df[column_name] = (months_df['Opportunity_Stage'] == stage).astype(int)

    # Group by Opportunity_ID and sum the stage occurrences
    result = months_df.groupby('Opportunity_ID').agg({f'Stage_Sum_{stage.replace(" ", "_").replace("/", "_").replace("-", "_")}': 'sum' for stage in stages}).reset_index()

    # Merge the result back into the original dataframe
    df = df.merge(result, on='Opportunity_ID')

    return df


def get_features(df):
    df = get_q_num(df)
    # df = df.drop('Quarter', axis=1)
    df = get_active_days(df)
    df = get_mos_stages(df)
    return df