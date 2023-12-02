# Protenus-Hackathon

### `generate_gt.py`
Generate ground-truth labels. `pred_q_correct` denotes that the row's `Opportunity_Close_Quarter` prediction was correct. `closed_next_q` denotes whether or not the deal was closed (positively **or** negatively -- we'll have to modify this for question 1) in the following quarter.  `pred_q_correct` denotes whether or not the deal was closed in the forecasted quarter, and `pred_q_plus_1_correct` denotes whether the deal was closed in the forcasted quarter *or* the quarter after.

