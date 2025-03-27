import numpy as np
import pickle
import seaborn as sns

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def sales_prediction(City, Customer_type, Gender, Product_line, Unit_price, Quantity, Rating):
    # Load trained models and encoders
    model = pickle.load(open("files/sales_prediction_model.pkl", 'rb'))
    encoder_dict = pickle.load(open("files/Sales_prediction_Encoder.pkl", 'rb'))
    inscaler = pickle.load(open("files/sales_prediction_inScaler.pkl", 'rb'))
    outscaler = pickle.load(open("files/sales_prediction_outScaler.pkl", 'rb'))

    # Encode categorical variables
    encoded_inputs = [
        encoder_dict["City"].transform([City])[0],
        encoder_dict["Customer type"].transform([Customer_type])[0],
        encoder_dict["Gender"].transform([Gender])[0],
        encoder_dict["Product line"].transform([Product_line])[0]
    ]

    # Convert input into a NumPy array
    input_data = np.array([[*encoded_inputs, Unit_price, Quantity, Rating]])

    # Scale input data
    scaled_input = inscaler.transform(input_data)

    # Predict sales
    prediction = model.predict(scaled_input)

    # Inverse transform the prediction
    inverse_scaled_pred = outscaler.inverse_transform(prediction.reshape(-1, 1))

    # Extract predicted sales amount
    sales_price = float(inverse_scaled_pred[0][0])  # Convert to float for safety

    # Create a dictionary for attributes
    attributes = {
        "City (Encoded)": encoded_inputs[0],
        "Customer Type (Encoded)": encoded_inputs[1],
        "Gender (Encoded)": encoded_inputs[2],
        "Product Line (Encoded)": encoded_inputs[3],
        "Unit Price": Unit_price,
        "Quantity": Quantity,
        "Rating": Rating,
        "Predicted Sales": sales_price
    }

    # Create a bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(attributes.keys()), y=list(attributes.values()), palette="viridis")

    # Annotate values on bars
    for index, value in enumerate(attributes.values()):
        plt.text(index, value + 0.05 * max(attributes.values()), f"{value:.2f}", ha='center', fontsize=10, fontweight='bold')

    # Add title and labels
    plt.xticks(rotation=30, ha='right', fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.title("Sales Prediction Analysis", fontsize=14, fontweight='bold')

    # Save the graph
    graph_path = "static/generated/sales_prediction_result.png"
    plt.savefig(graph_path, bbox_inches="tight")
    plt.close()

    return [f"{sales_price:.2f}", graph_path]  

# Example usage
predicted_sales, graph = sales_prediction('Mandalay','Member','Male','Health and beauty', 500, 2, 4.5)
print(predicted_sales)
print(f"Graph saved at: {graph}")
