# For the Predictions
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

The arrival buckets to be predicted are described in the submission_format.csv file and look like this:

     ID,Value
     KDEN_220925_0100_15,99
     KDEN_220925_0100_30,99
     KDEN_220925_0100_45,99
     KDEN_220925_0100_60,99
     KDEN_220925_0100_75,99
     ...
Where KDEN is the ICAO code for the airport, 220925 is the date (YYMMDD), 0100 is the time of the prediction (HHMM) and 15, 30,.. are the buckets into the future (from 1:00 to 1:15, from 1:15 to 1:30, etc.).
The order of the predictions should be the same as in the submission_format.csv file. Failing to follow this format will result in an error or lower score.

The evaluation metric is based on Root Mean Squared Error (RMSE). Specifically, it is calculated as exp(-RMSE/K), where K is a normalization factor of 10, and exp is the exponential function in order for it to be a number between 0.0 and 1.0, with 1.0 representing a perfect score (RMSE = 0).
