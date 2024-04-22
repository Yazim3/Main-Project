import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Function to read data from Excel file
def read_vehicle_data(filename="vehicledata.xlsx"):
    try:
        data_df = pd.read_excel(filename, engine='openpyxl')
        vehicle_data = data_df.set_index('VehicleType')['Count'].to_dict()
    except FileNotFoundError:
        messagebox.showerror("Error", "Data file not found.")
        vehicle_data = {}
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        vehicle_data = {}
    return vehicle_data

# Function to update the feature show list
def update_feat_show_list():
    data = read_vehicle_data()
    feat_show_list.delete(*feat_show_list.get_children())
    for vehicle_type, count in data.items():
        feat_show_list.insert("", tk.END, text=vehicle_type, values=(count,))

# Function to plot the vehicle count graph from the Excel data
def plot_graph():
    data = read_vehicle_data()
    if not data:
        messagebox.showinfo("No Data", "No data available for plotting.")
        return
    vehicle_types = list(data.keys())
    counts = list(data.values())

    plt.figure(figsize=(10, 5))
    plt.bar(vehicle_types, counts, color='skyblue')
    plt.xlabel('Vehicle Type')
    plt.ylabel('Count')
    plt.title('Vehicle Count by Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def toggle_feat_show():
    if feat_show.winfo_ismapped():
        feat_show.pack_forget()
    else:
        feat_show.pack(side=tk.LEFT, padx=10, pady=10)
        update_feat_show_list()

# Other necessary functions, including video handling and GUI setup
def update_video():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        video_label.imgtk = frame
        video_label.configure(image=frame)
        video_label.after(10, update_video)

def select_video():
    file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    if file_path:
        global cap
        cap = cv2.VideoCapture(file_path)
        update_video()

def set_selected_vehicle_type(event):
    global selected_vehicle_type
    selected_vehicle_type = vehicle_type_combobox.get()

# GUI initialization and layout code
root = tk.Tk()
root.title("Vehicle Count and Classification")
root.geometry("800x600")

# Sidebar
sidebar = tk.Listbox(root, bg="#1b1b1b", fg="white", selectbackground="cyan", font=("Arial", 14))
sidebar.insert(0, "Dashboard")
sidebar.insert(1, "Traffic")
sidebar.insert(2, "Report")
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Header frame
header_frame = tk.Frame(root, bg="#1abc9c")
header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
header_label = tk.Label(header_frame, text="KELTRON: VEHICLE COUNT AND CLASSIFICATION", bg="#1abc9c", fg="white", font=("Arial", 24))
header_label.pack(padx=10, pady=10)

# Main frame
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Video display
video_frame = tk.Frame(main_frame, bg="white")
video_frame.pack(side=tk.TOP, padx=10, pady=10)
video_label = tk.Label(video_frame)
video_label.pack()

select_video_button = tk.Button(main_frame, text="Select Video", command=select_video, bg="#3498db", fg="white", font=("Arial", 12))
select_video_button.pack(side=tk.TOP, padx=10, pady=10)

vehicle_type_combobox = ttk.Combobox(main_frame, values=["Car", "Bike", "Bus", "Truck", "3 Wheeler"], font=("Arial", 12))
vehicle_type_combobox.pack(side=tk.LEFT, padx=10, pady=10)
vehicle_type_combobox.set("All vehicle")  # Default selection
vehicle_type_combobox.bind("<<ComboboxSelected>>", set_selected_vehicle_type)

plot_graph_button = tk.Button(main_frame, text="Plot Vehicle Count Graph", command=plot_graph, bg="#e74c3c", fg="white", font=("Arial", 12))
plot_graph_button.pack(side=tk.LEFT, padx=10, pady=10)

# Feature display frame
feat_show = tk.Frame(main_frame, bg="#1e1e1e")
feat_show.pack_forget()

feat_show_list = ttk.Treeview(feat_show, columns=("Count"))
feat_show_list.heading("#0", text="Vehicle Type")
feat_show_list.heading("Count", text="Count")
feat_show_list.pack(side=tk.LEFT, padx=10, pady=10)

feat_btn = tk.Button(main_frame, text="Show Statistics", command=toggle_feat_show, bg="#2ecc71", fg="white", font=("Arial", 12))
feat_btn.pack(side=tk.TOP, padx=10, pady=10)

# Initialize video capture
cap = None
selected_vehicle_type = "Car"

root.mainloop()
