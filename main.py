import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import csv
import os
from time import time

data_dir = r'C:\Users\12392\Desktop\Sole Pressure Sensor/Data'


# Set up the serial connection
ser = serial.Serial('COM8', 9600, timeout=1)  # Update to the correct port

# Initialize the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=45, azim=45)
X, Y = np.meshgrid(range(5), range(3))
Z = np.zeros((3, 5))  # Initialize with zeros
surface = ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_zlim(0, 5)


# Function to update the Z data in the plot
def update(frame):
    global Z, surface, writer
    line = ser.readline().decode('utf-8').strip()
    if line:
        rows = line.split(';')
        for i, row in enumerate(rows):
            values = list(map(float, row.split(',')))
            Z[i] = values

        # Write the flattened Z matrix and timestamp to the CSV file
        timestamp = time()
        flat_values = [timestamp] + Z.flatten().tolist()
        writer.writerow(flat_values)

        # Print the 2D array to the terminal
        print("2D Array:")
        for row in Z:
            print(row)
        print()  # Newline for better readability

        # Update the surface plot 
        surface.remove()  # Remove the old surface
        surface = ax.plot_surface(X, Y, Z, cmap='viridis')  # Add updated surface

if __name__ == '__main__':

    start_time = time()

    os.makedirs(data_dir, exist_ok=True)

    file_name = f"PressureTest{int(start_time)}.csv"
    file_path = os.path.join(data_dir, file_name)

    with open(file_path, "w", newline="") as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(["Time, 0x0, 0x1, 0x2, 0x3, 0x4, 1x0, 1x1, 1x2, 1x3, 1x4, 2x0, 2x1, 2x2, 2x3, 2x4"])

        # Main function to run the animation
        try:
            ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False)
            plt.show()  # Keep running until interrupted
        except KeyboardInterrupt:
            print("Animation interrupted and gracefully stopped.")
            ser.close()  # Close the serial connection
