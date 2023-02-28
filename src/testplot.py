import matplotlib.pyplot as plt

# Create some sample data
positions = [10, 8, 6, 4]
distances = [2, 2, 2, 2]

# Plot the positions as circles
for i in range(len(positions)):
    plt.scatter(positions, [0]*4, s=100)
    plt.text(positions[i], -0.1, f"ACV{i}: {positions[i]}", ha='center', va='top')

# Add arrows to represent the distances
for i in range(0, len(positions) - 1):
    plt.arrow(positions[i+1], 0, distances[i+1], 0)
    plt.text((positions[i+1]+positions[i])/2, 0.1, f"{distances[i+1]}", ha='center', va='bottom')

# Set the x-axis limits
plt.xlim(0, 12)
plt.ylim(-1,1)

# Show the plot
plt.show()