#Data Pipeline Guidance

The project makes use of python and psycopg2 , SQL integration package for Redshift. Familiarity with the general concepts underlying Event based ingestion.


##Overview

The two primary Objective of this project are:
1. Create a scalable data pipeline to ingest JSON data to redshift schema
2. Centralized configuration config.ini of DB configuraton, table configuration, columns etc to make minimal changes in main program
	New table or columns can be added by tweaking configuration only :)


