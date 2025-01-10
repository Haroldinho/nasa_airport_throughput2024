# Bitgrit's NASA Airport Throughput Challenge
The NASA Airport Throughput Prediction Challenge is a challenge to forecast the number of arrivals at U.S. airports. [More details here](https://bitgrit.net/competition/23).

The Digital Information Platform (DIP) Sub-Project of Air Traffic Management - eXploration (ATM-X) is seeking to make available in the National Airspace System a variety of live data feeds and services built on that data. The goal is to allow external partners to build advanced, data-driven services using this data, and to make these services available to flight operators, who will use these capabilities to save fuel and avoid delays. Different wind directions, weather conditions at or near the airport, inoperative runways, etc., affect the runway configurations to be used and impact the overall arrival throughputs. Knowing the arrival runway and its congestion level ahead of time will enable aviation operators to perform better flight planning and improve flight efficiency. This competition seeks to make better predictions of runway throughputs using machine learning or other techniques. The total prize pool for this competition is $120,000.

This competition engages students, faculty members, and other individuals employed by United States universities to develop a machine learning model that provides a short-term forecast of estimated airport runway throughput using simulated real-time information from historical NAS and weather forecast data, as well as other factors such as meteorological conditions, airport runway configuration, and airspace congestion.


## Objective
My objective is to hone my skills at making forecasts for large time series datasets.
The work I want to undertake will involve:
- EDA 
- Anomaly Detection
- Dimensionality Reduction and Reduced Order Modeling
- Classical Forecating
- Deep Learning Based Forecasting techniques such as LSTM


## Competition Objective
**Predict throughput for a given airport and datetime  up to 3 hours in the future in 15 m**

Train and Test Split

For this challenge, the data has been split into Training and Testing via the following cyclical structure, starting from 2022/09/01:

Training: 24 days
Testing: 8 days
And so on, for an entire year of data.

Training Data: Training data contains (mostly) continuous information for all variables and can be used to train models. The models should be train so that, given an airport at a particular datetime, and the information (input data) available at that datetime for that airport (flights and weather, including future forecasts made at or before that datetime), the throughput of 15-min time buckets up to 3 hours into the future are used as target variable.
It is encouraged to create as many training examples as possible using this dataset.

Testing/Prediction Data: Testing data is the input data that should be used to make the predictions of this model. Because predictions must be made for 3 hours into the future for every timestamp T, this data is separated by 4-hour gaps that would contain the not yet available information 4 hours into the future of timestamp T. The first 3 of this 4 hours are the ones for which the throughput predictions should be made. For example, given a cycle of 8-days part of the testing data, the input data available for training the model would include data from 0:00 to 1:00 AM (to predict 1:00 to 4:00 AM), 5:00 to 6:00 (to predict 6:00 to 9:00 AM), and so on. This will be clearer when looking at the submission_format.csv file that is included in the dataset.
This is structured this way to ensure that no "future" information is available at time T regarding the next 3 hours, so that the data should be trained with whatever information is available at time T (including system estimates of arrivals into the future and weather forecasts made at or before time T).

The goal of the competition is to create real-time prediction models that can make inference without the use of any information that is not yet available, so this is very important to keep in mind when selecting the input data.