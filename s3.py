import boto3
import pandas as pd
s3 = boto3.client('s3')

s3 = boto3.resource(
    service_name='s3'
)
foo = pd.DataFrame({'x': [1, 2, 3], 'y': ['a', 'b', 'x']})
bar = pd.DataFrame({'x': [10, 20, 30], 'y': ['aa', 'bb', 'ccx']})
foo.to_csv('foo.csv')
bar.to_csv('bar.csv')

s3.Bucket('stockmodels9').upload_file(Filename='foo.csv', Key='foo.csv')
s3.Bucket('stockmodels9').upload_file(Filename='bar.csv', Key='bar.csv')

obj = s3.Bucket('stockmodels9').Object('foo.csv').get()
foo = pd.read_csv(obj['Body'], index_col=0)
print(foo)