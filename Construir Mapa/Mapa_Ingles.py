import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Path to the CSV file
file_path = r"C:\Users\caiod\OneDrive\Documentos\Projetos Python\IC\Imagens Finais\GEM CERN\Imagens"

# Read the CSV file
df = pd.read_csv(file_path + r"\Summary.csv")

# Get the image names, areas, and circularities
image_names = df.iloc[:, 1]  # Select column 1 (with names like X_2.33-Y_2.33)
a = df.iloc[:, 4]  # Select column 4 (areas)
areas = a.to_numpy()  # Convert the areas column to a NumPy array
radii = np.sqrt(areas / np.pi)  # Calculate the radii

# Get the circularity from column 7
circ = df.iloc[:, 7]  # Select column 7 (circularity)
circularities = circ.to_numpy()  # Convert the circularity column to a NumPy array

# Function to extract coordinates from the image name (e.g., X_2.33-Y_2.33)
def extract_coordinates(image_name):
    match = re.match(r"X_(\d+(\.\d+)?)\-Y_(\d+(\.\d+)?)", image_name)
    if match:
        x = float(match.group(1))
        y = float(match.group(3))
        return x, y
    return None, None

# Dictionary to store radii and circularities with their coordinates (X, Y)
coord_radii = {}
coord_circularities = {}

# Iterate over the image names and fill the dictionaries
for i, name in enumerate(image_names):
    x, y = extract_coordinates(name)
    if x is not None and y is not None:
        coord_radii[(x, y)] = radii[i]
        coord_circularities[(x, y)] = circularities[i]
    else:
        print(f"Failed to extract coordinates from {name}")

# Define grid dimensions
dim = 100
step = 2.359
dim_step = np.math.ceil(dim / step)

# Create matrices to store the radii and circularities values (heatmaps)
heatmap_radii = np.full((dim_step, dim_step), np.nan)  # Initialize with NaN
heatmap_circularities = np.full((dim_step, dim_step), np.nan)  # Initialize with NaN

# Fill the heatmaps based on the extracted coordinates
for (x, y), radius in coord_radii.items():
    i = int(np.round(x / step))  # Use np.round for better rounding
    j = int(np.round(y / step))
    
    # Check if the indices are within range
    if 0 <= i < dim_step and 0 <= j < dim_step:
        heatmap_radii[j, i] = radius
    else:
        print(f"Coordinates out of range: X={x}, Y={y}")

# Fill the circularity heatmap
for (x, y), circularity in coord_circularities.items():
    i = int(np.round(x / step))  # Use np.round for better rounding
    j = int(np.round(y / step))
    
    # Check if the indices are within range
    if 0 <= i < dim_step and 0 <= j < dim_step:
        heatmap_circularities[j, i] = circularity
    else:
        print(f"Coordinates out of range: X={x}, Y={y}")

# Function to display the heatmaps
def show_heatmaps():
    plt.figure(figsize=(10, 5))

    # Radii heatmap
    plt.subplot(1, 2, 1)
    plt.imshow(heatmap_radii, extent=[0, dim, 0, dim], origin='lower', cmap='viridis')
    plt.colorbar(label='Radius [µm]')
    plt.xlabel('X [mm]')
    plt.ylabel('Y [mm]')
    plt.title('GEM CERN Radius Map')

    # Circularity heatmap
    plt.subplot(1, 2, 2)
    plt.imshow(heatmap_circularities, extent=[0, dim, 0, dim], origin='lower', cmap='plasma')
    plt.colorbar(label='Circularity')
    plt.xlabel('X [mm]')
    plt.ylabel('Y [mm]')
    plt.title('GEM CERN Circularity Map')

    plt.tight_layout()
    plt.show()

# Function to display the histogram of radii
def show_radii_histogram():
    plt.figure()
    plt.hist(radii, bins=25, color='blue', edgecolor='black')
    plt.xlabel('Radius [µm]', fontsize=20)  # Increase the font size of the X-axis label
    plt.ylabel('Frequency', fontsize=20)  # Increase the font size of the Y-axis label
    plt.title('Radii Histogram', fontsize=25)  # Increase the font size of the title
    plt.xticks(fontsize=12)  # Increase the font size of X-axis ticks
    plt.yticks(fontsize=12)  # Increase the font size of Y-axis ticks
    plt.show()

# Function to display the histogram of circularities
def show_circularity_histogram():
    plt.figure()
    plt.hist(circularities, bins=13, color='yellow', edgecolor='black')
    plt.xlabel('Circularity', fontsize=20)  # Increase the font size of the X-axis label
    plt.ylabel('Frequency', fontsize=20)  # Increase the font size of the Y-axis label
    plt.title('Circularities Histogram', fontsize=25)  # Increase the font size of the title
    plt.xticks(fontsize=12)  # Increase the font size of X-axis ticks
    plt.yticks(fontsize=12)  # Increase the font size of Y-axis ticks
    plt.show()


# Display the plots in sequence
show_heatmaps()
show_radii_histogram()
show_circularity_histogram()
