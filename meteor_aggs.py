import boto3
import pandas as pd
import sys
import os
import logging
import argparse

def create_client(logger):
	try:
		logger.info(f'Creating S3 client.')
		client = boto3.client('s3')
		return client
	except ClientError as e:
		err_str = f'Error connecting to AWS and creating S3 client. Exception raised:\n{e}'
        logger.error(err_str)
		raise

def test_bucket(bucket, client, logger):
	try:
		logger.info(f'Making HEAD call to S3 bucket {bucket}.')
		response = client.head_bucket(Bucket=bucket)
	except (ClientError, NoSuchBucket) as e:
		err_str = f'Error making HEAD call to S3 bucket {bucket}. Exception raised:\n{e}'
		logger.error(err_str)
		raise

def build_key_list(bucket, client, logger):
	logger.info('Building key list.')
	test_bucket(bucket, client, logger)
	s3_keys = []
	continuation_token = 'check'
	while len(continuation_token) != 0:
		try:
			logger.info(f'Retrieving list of objects in {bucket}.')
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

	return raw_df

def clean_meteorite_data(bucket, logger):
	raw_df = generate_dataframe(bucket, logger)
	#####
	return cleaned_df

def final aggregations(bucket, logger):
	cleaned_df = clean_meteorite_data(bucket, logger)

	count_df = cleaned_df.groupby('year').year.agg(['count'])
	max_count = count_df['count'].max()
	max_years = count_df[(count_df['year'] == max_count)]

	avg_mass_string = str(cleaned_df['mass'].mean())
	max_years_string = ','.join(max_years)
	return avg_mass_string, max_years_string