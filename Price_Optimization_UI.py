import pickle
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def price_optimization(product_category, qty, unit_price, customers, lag_price):
    # Load trained models and encoders
    model = pickle.load(open("files/price_optimization_model.pkl", 'rb'))
    encoder = pickle.load(open("files/price_optimization_Encoder.pkl", 'rb'))
    inscaler = pickle.load(open("files/price_optimization_inScaler.pkl", 'rb'))
    outscaler = pickle.load(open("files/price_optimization_outScaler.pkl", 'rb'))

    # Encode categorical variable
    product_category_encoded = encoder.transform([product_category])[0]  

    # Calculate Total Price
    total_price = qty * unit_price  

    # Convert input into a NumPy array
    input_data = np.array([[product_category_encoded, qty, unit_price, customers, lag_price]])

    # Scale input data
    scaled_input = inscaler.transform(input_data)

    # Predict optimized price
    prediction = model.predict(scaled_input)

    # Inverse transform the prediction
    inverse_scaled_pred = outscaler.inverse_transform(prediction.reshape(-1, 1))

    # Extract the predicted optimized price
    optimized_price = inverse_scaled_pred[0][0]

    # Create a dictionary for all attributes (input & output)
    attributes = {
        "Product Category (Encoded)": product_category_encoded,
        "Quantity": qty,
        "Unit Price": unit_price,
        "Customers": customers,
        "Lag Price": lag_price,
        "Total Price": total_price,
        "Optimized Price": optimized_price
    }

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(attributes.keys()), y=list(attributes.values()), palette="viridis")

    # Annotate values on bars
    for index, value in enumerate(attributes.values()):
        plt.text(index, value + 0.05 * max(attributes.values()), f"{value:.2f}", ha='center', fontsize=10, fontweight='bold')

    # Add title and labels
    plt.xticks(rotation=20, ha='right', fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.title("Price Optimization Analysis", fontsize=14, fontweight='bold')

    # Save the graph
    graph_path = "static/generated/price_optimization_result.png"
    plt.savefig(graph_path, bbox_inches="tight")
    plt.close()

    return [f"{optimized_price:.2f}", f"{total_price:.2f}", graph_path ] 

# # Example usage
# optimized_price, total_price, graph = price_optimization('cool_stuff', 2, 78, 34, 89)
# print(optimized_price)  
# print(total_price)  
# print(f"Graph saved at: {graph}")  
