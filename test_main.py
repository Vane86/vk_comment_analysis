import pandas as pd

comments_clustered = pd.read_csv('comments_clustered.csv')
comments = pd.read_csv('data.csv')[['text', 'com_id']]

comments_clustered.set_index('com_id').join(comments.set_index('com_id')).to_csv('test.csv')
