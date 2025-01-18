import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Set up the serial connection
ser = serial.Serial('COM5', 9600, timeout=1)  # Update to the correct port

# Initialize the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=45, azim=45)
X, Y = np.meshgrid(range(5), range(3))
Z = np.zeros((3, 5))  # Initialize with zeros
surface = ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_zlim(0, 4095)


# Function to update the Z data in the plot
def update(frame):
    global Z, surface
    line = ser.readline().decode('utf-8').strip()
    if line:
        rows = line.split(';')
        for i, row in enumerate(rows):
            values = list(map(int, row.split(',')))
            Z[i] = values

        # Print the 2D array to the terminal
        print("2D Array:")
        for row in Z:
            print(row)
        print()  # Newline for better readability

        # Update the surface plot 
        surface.remove()  # Remove the old surface
        surface = ax.plot_surface(X, Y, Z, cmap='viridis')  # Add updated surface


# Main function to run the animation
try:
    ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False)
    plt.show()  # Keep running until interrupted
except KeyboardInterrupt:
    print("Animation interrupted and gracefully stopped.")
    ser.close()  # Close the serial connection
