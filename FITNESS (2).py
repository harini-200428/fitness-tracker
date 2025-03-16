import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Load dataset
data = pd.read_csv(r"C:\Users\ashwa\OneDrive\Desktop\AICET INTERNSHIP\exercise.csv")
data["Gender"] = data["Gender"].map({"male": 0, "female": 1})

# Create main window
root = tk.Tk()
root.title("Personal Fitness Tracker")
root.geometry("700x700")
root.configure(bg="#f0f8ff")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), background="#ffcc00", foreground="black", padding=10)
style.configure("TLabel", font=("Arial", 12), background="#f0f8ff", foreground="black")

label = tk.Label(root, text="🌟 Personal Fitness Tracker 🌟", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#ff6600")
label.pack(pady=20)

# Function to calculate BMI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # Convert cm to meters
        bmi = weight / (height ** 2)
        messagebox.showinfo("BMI Result", f"Your BMI is: {bmi:.2f}")
    except:
        messagebox.showerror("Error", "Invalid input! Enter numerical values.")

# Function to estimate calories burned
def estimate_calories():
    try:
        weight = float(weight_entry.get())
        duration = float(duration_entry.get())
        calories = (weight * 0.0175 * 6) * duration
        messagebox.showinfo("Calories Burned", f"Estimated Calories Burned: {calories:.2f} kcal")
    except:
        messagebox.showerror("Error", "Invalid input! Enter numerical values.")

# Function to show statistics
def show_statistics():
    avg_heart_rate = data["Heart_Rate"].mean()
    avg_bmi = (data["Weight"] / ((data["Height"] / 100) ** 2)).mean()
    stats_msg = f"Average Heart Rate: {avg_heart_rate:.2f} bpm\nAverage BMI: {avg_bmi:.2f}"
    messagebox.showinfo("User Statistics", stats_msg)

# Function to export data
def export_data():
    data.to_excel("fitness_data.xlsx", index=False)
    messagebox.showinfo("Export Successful", "Data exported to fitness_data.xlsx")

# Function to show different graphs
def show_graph(option):
    plt.figure(figsize=(8, 5))
    if option == "Heart Rate vs Duration":
        plt.scatter(data["Duration"], data["Heart_Rate"], color="blue", label="Heart Rate")
        plt.xlabel("Duration (minutes)")
        plt.ylabel("Heart Rate (bpm)")
        plt.title("Heart Rate vs Duration")
    elif option == "BMI Distribution":
        bmi = data["Weight"] / ((data["Height"] / 100) ** 2)
        plt.hist(bmi, bins=10, color="green", alpha=0.7)
        plt.xlabel("BMI")
        plt.ylabel("Frequency")
        plt.title("BMI Distribution")
    plt.legend()
    plt.grid()
    plt.show()

# Function to predict heart rate using multiple factors
def predict_heart_rate():
    X = data[["Duration", "Age", "Weight"]]
    y = data["Heart_Rate"]
    
    model = LinearRegression()
    model.fit(X, y)
    
    future_duration = float(duration_entry.get())
    age = float(age_entry.get())
    weight = float(weight_entry.get())
    predicted_heart_rate = model.predict([[future_duration, age, weight]])[0]
    
    messagebox.showinfo("Prediction Result", f"Predicted Heart Rate: {predicted_heart_rate:.2f} bpm")

# Input fields for BMI, Calories, and Prediction
frame = ttk.Frame(root)
frame.pack(pady=10)

ttk.Label(frame, text="Height (cm):").grid(row=0, column=0)
height_entry = ttk.Entry(frame)
height_entry.grid(row=0, column=1)

ttk.Label(frame, text="Weight (kg):").grid(row=1, column=0)
weight_entry = ttk.Entry(frame)
weight_entry.grid(row=1, column=1)

ttk.Label(frame, text="Age:").grid(row=2, column=0)
age_entry = ttk.Entry(frame)
age_entry.grid(row=2, column=1)

ttk.Label(frame, text="Duration (min):").grid(row=3, column=0)
duration_entry = ttk.Entry(frame)
duration_entry.grid(row=3, column=1)

# Buttons
btn_bmi = ttk.Button(root, text="📏 Calculate BMI", command=calculate_bmi, style="TButton")
btn_bmi.pack(pady=5)

btn_calories = ttk.Button(root, text="🔥 Estimate Calories Burned", command=estimate_calories, style="TButton")
btn_calories.pack(pady=5)

btn_stats = ttk.Button(root, text="📊 Show Statistics", command=show_statistics, style="TButton")
btn_stats.pack(pady=5)

btn_export = ttk.Button(root, text="📂 Export Data to Excel", command=export_data, style="TButton")
btn_export.pack(pady=5)

# Graph Dropdown
graph_options = ["Heart Rate vs Duration", "BMI Distribution"]
selected_graph = tk.StringVar()
graph_menu = ttk.Combobox(root, values=graph_options, textvariable=selected_graph)
graph_menu.pack(pady=5)
graph_menu.set("Select Graph")
ttk.Button(root, text="📉 Show Graph", command=lambda: show_graph(selected_graph.get()), style="TButton").pack(pady=5)

btn_predict = ttk.Button(root, text="❤️ Predict Future Heart Rate", command=predict_heart_rate, style="TButton")
btn_predict.pack(pady=5)

btn_exit = ttk.Button(root, text="❌ Exit", command=root.quit, style="TButton")
btn_exit.pack(pady=10)

root.mainloop()
