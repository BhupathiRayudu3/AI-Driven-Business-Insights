import numpy as np
import pickle
import pandas as pd

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns

def forecast_revenue(fixed_date, varying_date, sequence_length, future_steps):
    # Load the trained model and scaler
    model = pickle.load(open("files/revenue_prediction_model.pkl", 'rb'))
    scaler = pickle.load(open("files/revenue_prediction_Scaler.pkl", 'rb'))

    revenue_data = pd.read_csv("files/applerevenue.csv")
    revenue_data['date'] = pd.to_datetime(revenue_data['date'], format="%d-%m-%Y")
    revenue_data.set_index('date', inplace=True)

    data = revenue_data['open'].values.reshape(-1, 1)
    scaled_data = scaler.transform(data)

    # Ensure dates are in datetime format
    fixed_date = pd.to_datetime(fixed_date)
    varying_date = pd.to_datetime(varying_date)

    # Extract the last known sequence for prediction
    revenue_data.index = pd.to_datetime(revenue_data.index)
    future_data = scaled_data[-sequence_length:]  # Ensure correct sequence length

    future_predictions = []
    for _ in range(future_steps):  
        input_data = future_data[-sequence_length:].reshape(1, sequence_length, 1)
        prediction = model.predict(input_data)
        future_predictions.append(prediction[0][0])
        
        # Append new prediction while keeping sequence length constant
        future_data = np.append(future_data[-(sequence_length - 1):], prediction)

    # Inverse transform to get actual values
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    # Generate future dates
    last_date = revenue_data.index.max()
    future_dates = [last_date + pd.DateOffset(days=i) for i in range(1, future_steps + 1)]

    # Create a DataFrame for results
    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted Revenue": future_predictions.flatten()})

    # Plot the predictions
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=revenue_data, x=revenue_data.index, y="open", label="Actual Revenue", color="blue")
    sns.lineplot(data=forecast_df, x="Date", y="Predicted Revenue", label="Predicted Revenue", color="red", linestyle="dashed")

    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.title("Revenue Forecasting")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    graph_path = "static/generated/revenue_prediction_result.png"
    plt.savefig(graph_path, bbox_inches="tight")
    plt.close()
    plt.show()

    return forecast_df,graph_path

# Example usage
forecast_df = forecast_revenue("2022-10-28", "2022-11-01", sequence_length=10, future_steps=30)
print(forecast_df)
