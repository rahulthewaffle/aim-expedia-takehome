import boto3
import pandas as pd
import sys
import os
import logging
import argparse

# Creating S3 client.
def create_client(logger):
	try:
		client = boto3.client('s3')
		return client
	except ClientError as e:
		err_str = f'Error connecting to AWS and creating S3 client. Exception raised:\n{e}'
        logger.error(err_str)
		raise

# Validating access to S3 bucket bucket.
def test_bucket(bucket, client, logger):
	try:
		response = client.head_bucket(Bucket=bucket)
	except (ClientError, NoSuchBucket) as e:
		err_str = f'Error making HEAD call to S3 bucket {bucket}. Exception raised:\n{e}'
		logger.error(err_str)
		raise

# Retrieving list of objects in bucket.
def build_key_list(bucket, client, logger):
	test_bucket(bucket, client, logger)
	
	s3_keys = []
	continuation_token = 'check'

	while len(continuation_token) != 0:
		try:
			response = client.list_objects_v2(Bucket=bucket)
		except (ClientError, NoSuchBucket) as e:
			err_str = f'Error listing objects in S3 bucket {bucket}. Exception raised:\n{e}'
			logger.error(err_str)
			raise

		contents = response.get('Contents')
		continuation_token = response.get('NextContinuationToken')

		for x in contents:
			key = x.get('key')
			s3_keys.append(key)

	key_count = str(len(s3_keys))
	logger.debug(f'Retrieved {key_count} keys from {bucket}:\n{keys}')
	return s3_keys

# Reading meteorite JSONs and generating unprocessed dataframe.
def generate_dataframe(bucket, logger):
	client = create_client(logger)
	s3_keys = build_key_list(bucket, client, logger)

	raw_df = pd.DataFrame()

	for key in s3_keys:
		try:
			response = client.get_object(Bucket=bucket, Key=key)
		except (ClientError, NoSuchKey, InvalidObjectState) as e:
			err_str = f'Failed to retrieve S3 object {key} from {bucket}. Exception raised:\n{e}'
			logger.error(err_str)
			raise

		payload = response.get('Body')
		raw_df = raw_df.append(pd.read_json(payload))

	logger.debug(f'Unprocessed dataframe shape: {raw_df.shape}.')
	logger.debug(raw_df.head(5))
	return raw_df

# Cleaning unprocessed dataframe.
def clean_meteorite_data(bucket, logger):
	raw_df = generate_dataframe(bucket, logger)

	cleaned_df = raw_df[['name', 'id', 'mass', 'fall', 'year']]
	cleaned_df = cleaned_df.convert_dtypes().dropna()
	cleaned_df['year'] = clenaed_df['year'].apply(lambda x:x[0:4])[0]
	cleaned_df = cleaned_df[(cleaned_df['fall'] == 'Fell')]

	logger.debug(f'Cleaned dataframe shape: {cleaned_df.shape}')
	logger.debug(cleaned_df.head(5))
	return cleaned_df

def final aggregations(bucket, logger):
	cleaned_df = clean_meteorite_data(bucket, logger)

	count_df = cleaned_df.groupby('year').year.agg(['count'])
	max_count = count_df['count'].max()
	max_years = count_df[(count_df['year'] == max_count)]

	avg_mass_string = str(cleaned_df['mass'].mean())
	max_years_string = ','.join(max_years)
	return avg_mass_string, max_years_string