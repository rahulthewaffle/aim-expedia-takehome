import boto3
import pandas as pd
import sys
import os
import logging
import argparse

def create_client(logger):
	try:
		client = boto3.client('s3')
		logger.info(f'Attempting to connect to AWS and create S3 client.')
	except Exception as e:
		exc_str = f'Error connecting to AWS and creating S3 client. Exception raised:\n{e}'
        logger.exception(exc_str)
		raise

def test_bucket_connection(bucket, client, logger):
	response = client.head_bucket(Bucket=bucket)
	


def build_key_list(bucket, client, logger):
	if test_bucket_connection(bucket, client, logger):
		########
		return s3_keys

def generate_dataframe(bucket, logger):
	client = create_client(logger)
	s3_keys = build_key_list(bucket, client, logger)

	raw_df = pd.DataFrame()

	for key in s3_keys:
		response = client.get_object(Bucket=bucket, Key=key)

		status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
		if status != 200:
			err_str = f'Failed to retrieve S3 object {key} from {bucket}. Status:\n{status}'
			logger.error(err_str)
			raise ValueError(err_str)

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