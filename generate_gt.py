import pandas as pd
import numpy as np

def generate_labels():
    df = pd.read_csv('Protenus Sales Training Data.csv', low_memory=False)
    df['Snapshot_Date'] = pd.to_datetime(df['Snapshot_Date'], format='%m/%d/%y')
    df['Opportunity_Created_Date'] = pd.to_datetime(df['Opportunity_Created_Date'], format='%m/%d/%y')
    df['Opportunity_Close_Date'] = pd.to_datetime(df['Opportunity_Close_Date'], format='%m/%d/%y')

    def get_quarter_year_from_date(date):
        return 'Q' + str(date.quarter) + '-' + str(date.year)

    df['Snapshot_Quarter'] = df['Snapshot_Date'].apply(get_quarter_year_from_date)
    df['Opportunity_Close_Quarter'] = df['Opportunity_Close_Date'].apply(get_quarter_year_from_date)


    df['true_close_q'] = None

    for index, curr_row in df.iterrows():
        curr_id = curr_row['Opportunity_ID']
        pred_close_q = curr_row['Opportunity_Close_Quarter']

        curr_opp_df = df[df['Opportunity_ID'] == curr_id].copy()

        closed_row = curr_opp_df[(curr_opp_df['Opportunity_Stage'] == 'Closed Won') | \
                                (curr_opp_df['Opportunity_Stage'] == 'Closed Lost')]
        
        if len(closed_row) > 0:
            true_close_q = closed_row['Opportunity_Close_Quarter'].values[0]
            df.loc[index, 'true_close_q'] = true_close_q

    df['pred_q_correct'] = df['true_close_q'] == df['Opportunity_Close_Quarter']
    df['pred_q_correct'] = df['pred_q_correct'].astype(int)

    def add_one_quarter(date_str):
        quarter = int(date_str[1])
        year = int(date_str[3:])
        if quarter == 4:
            quarter = 1
            year += 1
        else:
            quarter += 1
        return 'Q' + str(quarter) + '-' + str(year)

    df['next_quarter'] = df['Snapshot_Quarter'].apply(add_one_quarter)
    df['closed_next_q'] = df['Opportunity_Close_Quarter'] == df['next_quarter']
    df['closed_next_q'] = df['closed_next_q'].astype(int)
    df['pred_q_plus_1_correct'] = (df['true_close_q'] == df['next_quarter']) | (df['pred_q_correct'] == 1)

    return df
