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

# environment setup

Per verbal instructions, this code is written to be run locally.
Depdencies and specific versions used can be found in `dependencies.txt`.
Although it shouldn't matter, I would recommend running this code in a separate environment using venv or conda.

# configuration and running

Logging is set to a default local directory `logs/log_<datetime>.log`. Via CLI argument, this can be changed.
	Since it is only intended to be run locally, this code does not support writing logs to an S3 instance.
The ingested S3 bucket is similarly customizable and defaults to `majorly-meteoric`.
If the default options are fine, running the code is as simple as typing `python meteor_aggregations.py` in your CLI and hitting enter.