import numpy as np
import pickle
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def profit_prediction(RD_Spend, Administration, Marketing_Spend, State):
    # Load trained models and encoders
    model = pickle.load(open("files/profit_prediction_model.pkl", 'rb'))
    encoder = pickle.load(open("files/profit_prediction_Encoder.pkl", 'rb'))
    inscaler = pickle.load(open("files/profit_prediction_inScaler.pkl", 'rb'))
    outscaler = pickle.load(open("files/profit_prediction_outScaler.pkl", 'rb'))

    # # Encode categorical variable (State)
    state_encoded = encoder.transform([State])[0]

    # Convert input into NumPy array
    input_data = np.array([[RD_Spend, Administration, Marketing_Spend, state_encoded]])

    # Scale input data
    scaled_input = inscaler.transform(input_data)

    # Predict profit
    prediction = model.predict(scaled_input)

    # Inverse transform the prediction
    inverse_scaled_pred = outscaler.inverse_transform(prediction.reshape(-1, 1))  

    # Extract profit prediction
    profit_price = float(inverse_scaled_pred)#[0][0])  # Convert to float for safety

    # Create a dictionary for all attributes 
    attributes = {
        "R&D Spend": RD_Spend,
        "Administration": Administration,
        "Marketing Spend": Marketing_Spend,
        "State": state_encoded,
        "Profit Price": profit_price
    }

    # Create a bar plot (excluding State)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(attributes.keys()), y=list(attributes.values()), palette="viridis")

    # Annotate values on bars
    for index, value in enumerate(attributes.values()):
        plt.text(index, value + 0.05 * max(attributes.values()), f"{value:.2f}", ha='center', fontsize=10, fontweight='bold')

    # Add title and labels
    plt.xticks(rotation=20, ha='right', fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.title(f"Profit Prediction Analysis ({State})", fontsize=14, fontweight='bold')

    # Save the graph
    graph_path = "static/generated/profit_prediction_result.png"
    plt.savefig(graph_path, bbox_inches="tight")
    plt.close()

    return [f"{profit_price:.2f}", graph_path ] 

# Example usage
optimized_price, graph = profit_prediction(165349.20, 136897.800, 471784.1000, 'California')
print(optimized_price)  
print(f"Graph saved at: {graph}")  