import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

class DSU:
    def __init__(self, n=None):
        if n is not None:
            self.init(n)
        
    def init(self, n):
        self.f = list(range(n))
        self.siz = [1] * n
    
    def find(self, x):
        # Path compression heuristic
        if self.f[x] != x:
            self.f[x] = self.find(self.f[x])
        return self.f[x]
    
    def same(self, x, y):
        return self.find(x) == self.find(y)
    
    def merge(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.siz[x] < self.siz[y]:
            x, y = y, x
        self.siz[x] += self.siz[y]
        self.f[y] = x
        return True
    
    def size(self, x):
        return self.siz[self.find(x)]

# Define a function to generate distinct colors
def generate_color_map(num_colors):
    color_map = []
    for i in range(num_colors):
        hue = i * (360.0 / num_colors)
        saturation = 0.6
        value = 0.9
        color = np.array([hue, saturation, value])
        color_rgb = hsv_to_rgb(color)
        color_map.append(color_rgb)
    return color_map

# Convert HSV color to RGB
def hsv_to_rgb(color):
    hue, saturation, value = color
    hi = np.floor(hue / 60.0) % 6
    f = hue / 60.0 - np.floor(hue / 60.0)
    value = value * 255
    v = value
    p = value * (1 - saturation)
    q = value * (1 - f * saturation)
    t = value * (1 - (1 - f) * saturation)
    if hi == 0:
        return [v, t, p]
    elif hi == 1:
        return [q, v, p]
    elif hi == 2:
        return [p, v, t]
    elif hi == 3:
        return [p, q, v]
    elif hi == 4:
        return [t, p, v]
    else:
        return [v, p, q]
def convert_to_gradient_image(image_path):
    # Read the image
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply the Sobel operator for gradient computation
    gradient_x = cv2.Sobel(original_image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(original_image, cv2.CV_64F, 0, 1, ksize=3)

    # Calculate the magnitude of the gradients
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)

    # Normalize the gradient magnitude to the range [0, 255]
    gradient_magnitude = cv2.normalize(
        gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX
    )

    # Convert to uint8 for display
    gradient_image = np.uint8(gradient_magnitude)

    return gradient_image

def marker_coordinates(input_image_path):
    def get_coordinates(event):
        if event.button == 1:  # Left mouse button click
            x = int(round(event.xdata))
            y = int(round(event.ydata))
            coordinates.append((y, x))  # Append coordinates in (row, col) format
            plt.scatter(x, y, color='red')
            plt.draw()

    image = plt.imread(input_image_path)
        
    if image is None:
        print("Error: Could not open or find the image.")
        exit()

    # Ask user for the number of markers
    # num_markers = int(input("Enter the number of markers: "))

    global coordinates
    coordinates = []

    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_title('Click to select markers')
    plt.connect('button_press_event', get_coordinates)

    plt.show()
    return coordinates
