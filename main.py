import pandas as pd

comments = pd.concat((pd.read_csv('test_data/comments_0-2000.csv'),
                      pd.read_csv('test_data/comments_2000-7000.csv'),
                      pd.read_csv('test_data/comments_7000-12000.csv'),
                      pd.read_csv('test_data/comments_12000-17000.csv'),
                      pd.read_csv('test_data/comments_17000-22000.csv'),
                      pd.read_csv('test_data/comments_22000-27000.csv'),
                      pd.read_csv('test_data/comments_27000-30000.csv')), axis=0)
comments.drop_duplicates().to_csv('comments_0-30000.csv')
