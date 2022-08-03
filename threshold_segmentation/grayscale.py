from PIL import Image
from scipy import misc
import numpy as np


# function to convert an rgb image to grayscale image
def grayscale_conversion(path):
   image = Image.open(path)     
   image = np.array(image)
   height, width, channels = image.shape
   grayscale_image = np.zeros((height, width), dtype = np.uint8)

   for i in range(0, height):
      for j in range(0, width):
         r, g, b = image[i, j, 0], image[i, j, 1], image[i, j, 2]
         #convert image to grayscale with luma method Y = 0.2126R + 0.7152 + 0.0722B
         grayscale_image[i, j] = 0.2126*r + 0.7152*g + 0.0722*b
    
   return Image.fromarray(grayscale_image)
     

def grayscale_histogram(grayscale_image):
   grayscale_image = np.array(grayscale_image)
   height, width = grayscale_image.shape
   histogram = np.zeros(256, dtype = np.uint8)
   k = 0
   for i in range(0, height):
      for j in range(0, width):
         k = grayscale_image[i, j]
         histogram[k] = histogram[k] + 1

   return histogram

