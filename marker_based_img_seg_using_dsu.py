import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import os
from utility_fxns import generate_color_map, convert_to_gradient_image, DSU

THRESHOLD = 10

def segment_image(input_image_path, coordinates):
    gradient_image = convert_to_gradient_image(input_image_path)
    output_image_path = input_image_path.rsplit('.',1)[0] + "_gradient.jpg"
    cv2.imwrite(output_image_path, gradient_image)
    gradient_image = mpimg.imread(output_image_path).astype(int)
    gradient_image = gradient_image.copy()
    org_image = mpimg.imread(input_image_path).copy()
    
    width = len(gradient_image[0])
    height = len(gradient_image)

    dsu = DSU(height * width)
    visited = np.zeros((height, width), dtype=bool)

    def value_check(r1, c1, r2, c2):
        return (gradient_image[r1, c1] <= THRESHOLD and gradient_image[r2, c2] <= THRESHOLD)

    def dfs(row, col):
        stack = [(row, col)]
        visited[row, col] = True
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        while stack:
            r, c = stack.pop()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < height and 0 <= nc < width and not visited[nr, nc] and value_check(r, c, nr, nc):
                    if dsu.merge(r * width + c, nr * width + nc):
                        visited[nr, nc] = True
                        stack.append((nr, nc))

    num_markers = len(coordinates)
    colors = generate_color_map(num_markers)
    groups = dict()
    i=0
    for (row, col) in coordinates:
        # print("row: ", row)
        # print("col: ", col)
        # print(row, col)
        # row=int(row)
        # col=int(col)
        if visited[row][col]:
            continue
        dfs(row, col)
        groups[dsu.find(row * width + col)] = colors[i]
        i+=1

    # print("groups: ", groups)
    for i in range(height):
        for j in range(width):
            if visited[i][j]:
                # print("key: ", dsu.find(i * width + j))
                org_image[i][j] = groups[dsu.find(i * width + j)]
            # else:
            #     org_image[i][j] = [255, 255, 255]
    output_image_path = input_image_path.rsplit('.',1)[0] + "_segmented.jpg"
    # output_zip_image_path=input_image_path.rsplit('.',1)[0] + "_segmented.zip"
    # Remove the existing segmented image if it exists
    if os.path.exists(output_image_path):
        os.remove(output_image_path)
    org_image = cv2.cvtColor(org_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_image_path, org_image)
    #zipping the segmented image
    # import zipfile
    # with zipfile.ZipFile(output_zip_image_path, 'w') as zipf:
    #     zipf.write(output_image_path)
    plt.imshow(mpimg.imread(output_image_path))
    plt.show()
    return output_image_path
