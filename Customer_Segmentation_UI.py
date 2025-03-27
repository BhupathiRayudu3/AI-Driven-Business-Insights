import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Function to predict a single customer
def predict_new_customer(single_customer):
    """
    Predicts the cluster for a single customer and visualizes the result.
    :param single_customer: Dictionary with customer data (must match original features)
    :return: Predicted cluster number
    """
    model = pickle.load(open("files/Customer_segmentation_model.pkl", 'rb'))
    label_encoders = pickle.load(open("files/Customer_segmentation_Encoder.pkl", 'rb'))
    scaler = pickle.load(open("files/Customer_segmentation_Scaler.pkl", 'rb'))
    pca = pickle.load(open("files/Customer_segmentation_PCA.pkl", 'rb'))


    data = pd.read_csv("files/supervised_customer_segments.csv")
    single_df = pd.DataFrame([single_customer])

    categorical_cols = ["title", "gender", "country", "department", "job_title", "language"]
    
    # Encode categorical variables
    for col in categorical_cols:
        if col in single_df.columns and col in label_encoders:
            single_df[col] = label_encoders[col].transform(single_df[col].astype(str))
    
    # Scale numerical data
    single_scaled = scaler.transform(single_df.select_dtypes(include=[np.number]))
    
    # Predict cluster
    cluster = model.predict(single_scaled)[0]
    cluster_name = f"Cluster {cluster+1}"
    
    # Plot the result
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=data["PCA1"], y=data["PCA2"], hue=data['Cluster'], palette="viridis", s=50, alpha=0.5)
    single_pca = pca.transform(single_scaled)
    plt.scatter(single_pca[:, 0], single_pca[:, 1], color='red', marker='X', s=200, label='New Customer')
    plt.title("Single Customer Segmentation")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    # Add legend
    plt.legend()

    # Save the plot to a file (no GUI)
    output_path = "static/generated/new_customer_result.png"
    plt.savefig(output_path)

    # Close the plot to free up memory (important for Flask to avoid memory issues)
    plt.close()

    # Return the path for serving the image
    return [cluster_name, output_path]


# Example single customer prediction
single_customer = single_customer = {
    "title": "Honorable",
    "gender": "Agender",
    "country": "Zambia",
    "latitude": -17.473886,
    "longitude": 24.295514,
    "department": "Support",
    "job_title": "Internal Auditor",
    "language": "Indonesian"
}  

# predicted_cluster = predict_new_customer(single_customer)
# print(predicted_cluster)