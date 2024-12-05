# Databricks notebook source
# MAGIC %md
# MAGIC # Exploring the datasets
# MAGIC - FUSER
# MAGIC - METAR
# MAGIC - Terminal Aerodrome Forecast (TAF)
# MAGIC - Convective Weather Avoidance Model (CWAM)
# MAGIC
# MAGIC Save the result of the initial exploration into delta live tables for quick access

# COMMAND ----------

# MAGIC %md
# MAGIC ## Locate files in mounted DBFS

# COMMAND ----------

dbutils.fs.ls("dbfs:/mnt/nasa_challenge/1-raw-unzipped-files/")

# COMMAND ----------

# MAGIC %md
# MAGIC ## FUSER
# MAGIC  The fuser data is airport specific:
# MAGIC  - KATL (Atlanta)
# MAGIC  - KCLT (Charlotte)
# MAGIC  - KDEN (Denver)
# MAGIC  - KDFW (Dallas Fort Worth)
# MAGIC  - KJFK (New York JFK)
# MAGIC  - KMEM (Memphis)
# MAGIC  - KORD (Chicago O'Hare)
# MAGIC  - KPHX (Phoenix)
# MAGIC  - KSEA (Seattle)
# MAGIC
# MAGIC  The data also contains the test set *FUSER_test*
# MAGIC

# COMMAND ----------

dbutils.fs.ls("dbfs:/mnt/nasa_challenge/1-raw-unzipped-files/FUSER_train_KATL/KATL/")

# COMMAND ----------

# MAGIC %md
# MAGIC FUSER data can be further broken down into: 
# MAGIC - Configs Data Set (D-ATIS Data) -- configs_data_set
# MAGIC - Runways Data Set (Arrival Departure Detection) TARGET. --runways_data_set
# MAGIC - First Position Data Set -- first_position_data_set
# MAGIC - TBFM Data Set (Time-Based Flow Management Data) -- TBFM_data_set
# MAGIC - TFM Track Data Set (Traffic Flow Management Data) -- TFM_track_data_set
# MAGIC - ETD Data Set (Estimated Time of Departure) -- ETD_data_set
# MAGIC - LAMP Data Set (Local Aviation MOS Program Data) -- LAMP_data_set
# MAGIC - MFS Data Set (FAA SWIM Feeds) -- MFS_data_set

# COMMAND ----------

fuser_data_types = [
    'configs_data_set',
    'runways_data_set',
    'first_position_data_set',
    'TBFM_data_set',
    'TFM_track_data_set',
    'ETD_data_set',
    'LAMP_data_set',
    'MFS_data_set',
]
fuser_df = {}

# COMMAND ----------

for fuser_data_type in fuser_data_types:
    fuser_df[fuser_data_type] = spark.read.csv(f"dbfs:/mnt/nasa_challenge/1-raw-unzipped-files/FUSER_train_KATL/KATL/*.{fuser_data_type}.csv", header=True, inferSchema=True)

# COMMAND ----------

for fuser_data_type, df in fuser_df.items():
    num_rows = df.count()
    column_names = df.columns
    # num_distinct_dates = df.select("date_column").distinct().count()  # Replace "date_column" with the actual date column name
    print(f"Data Type: {fuser_data_type}")
    print(f"Number of Rows: {num_rows}")
    print(f"Column Names: {column_names}")
    # print(f"Number of Distinct Dates: {num_distinct_dates}")
    print("-" * 40)

# COMMAND ----------

fuser_df['configs_data_set'].describe()

# COMMAND ----------


