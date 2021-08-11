# aim-expedia-takehome

Code and documentation for Expedia/AIM Takehome Project

# about

This code ingests a modest quantity of data from S3 on meteorite impacts (\~11 MB) and prints two aggregations:
	- Average Meteorite Mass
	- Year with Highest Count of Meteorite Impacts (`fall status attribute == "Fell"`)

# assumptions

The code assumes consistency in the input schema, and based on exploration of the provided data, assumes consistency in the timestamp format.

Rows with null/empty values in the `name`, `year`, and `fall` columns are discarded without interpolation or substitution.

No logic is built around the `nametype == "Valid"` attribute.

In order to retrieve the JSON buckets from S3, the code first generates a list of S3 objects. To do this, two assumptions are made:
- Input data names follows the regex pattern of `data[0-9]*\.json`.
- Between the time that an object name is listed and the time the object is retrieved, the object's availability in the bucket has not changed. If a bucket cannot be retrieved when using the key yielded in the API call `list_objects_v2`, an error is logged and an exception raised, with recommendation to validate the S3 permissions and retry.
- The S3 bucket does not contain objects with duplicate keys.

# environment setup

Per verbal instructions, this code is written to be run locally.

Filepaths are flexible for use in both Unix and Windows.

In order for the code's boto3 calls to access S3, you will need to install the aws CLI and provide your access credentials via the `aws configure` command.
	This is preferable to hard-coding credentials, and equivalent to using and configuring a local `credentials.ini` file.

Python depdencies and specific versions used can be found in `dependencies.txt`.

Although it shouldn't matter, I would recommend running this code in a separate Python environment using venv or conda.

# configuration and running

Logging is set to a default local directory `tmp/logs/log_<datetime>.log`. Via CLI argument, this can be changed.
- Since it is only intended to be run locally, this code does not support writing logs to an S3 instance. This is a simple implementation if required.

The ingested S3 bucket can be similarly set as `--bucket` and defaults to `majorly-meteoric`.

If the default options are fine, running the code is as simple as opening your CLI, `cd`ing to the directory where you've downloaded my python script, typing `python meteor_aggregations_main`, and hitting enter.