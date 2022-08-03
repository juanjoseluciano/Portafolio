from PIL import Image
import numpy as np


#function to binarize image with Isodata Threshold
def isodata_threshold(grayscale_image, histogram):      
   grayscale_image = np.array(grayscale_image)
   height, width = grayscale_image.shape   
   binary_image = np.zeros((height, width), dtype = np.uint8)
   k = len(histogram)
   q = 0
   q = int(_mean(histogram, 0, k))
         
   while True:
      n0 = _count(histogram, 0, q)
      n1 = _count(histogram, q+1, k)

      if (n0 == 0) or (n1 == 0):
         return -1
     
      mu0 = _mean(histogram, 0, q)
      mu1 =  _mean(histogram, q + 1, k)
      q1 = q
      q = int((mu0 + mu1) / 2)

      if q == q1:
         break


   #image binarization
   for i in range(0, height):
      for j in range(0, width):
         if grayscale_image[i, j] <= q:
            binary_image[i, j] = 255
         else:
            binary_image[i, j] = 0

   return Image.fromarray(binary_image)

def _count(histogram, a, b):
   c = 0
   
   for g in range(a, b):
      c = c + histogram[g]

   return c         
            
def _mean(histogram, a, b):
   q1 = 0
   q2 = 0
   
   for g in range(a, b):
      q1 = (q1 + (g * histogram[g]))
      q2 = (q2 + histogram[g])

   return (q1 / q2)
 
#function to binarize image using Fast Isodata Threshold
def fast_isodata_threshold(grayscale_image, histogram):
   grayscale_image = np.array(grayscale_image)
   height, width = grayscale_image.shape   
   binary_image = np.zeros((height, width), dtype = np.uint8)
   k = len(histogram)
   mu0, mu1, N = _make_mean_tables(histogram)
   q = mu0[k - 1]
   
   while True:         
      if (mu0[int(q)] < 0) or (mu1[int(q)] < 0):
         return -1
     
      q1 = q
      q = int((mu0[int(q)] + mu1[int(q)])) / 2
      
      if q == q1:
         break

   #image binarization
   for i in range(0, height):
      for j in range(0, width):
         if grayscale_image[i, j] <= q:
            binary_image[i, j] = 255
         else:
            binary_image[i, j] = 0

   return Image.fromarray(binary_image)      

#function to binarize image using Otsu's method
def otsu_threshold(grayscale_image, histogram):
   grayscale_image = np.array(grayscale_image)
   height, width = grayscale_image.shape
   binary_image = np.zeros((height, width), dtype = np.uint8)      
   k = len(histogram)
   mu0, mu1, MN = _make_mean_tables(histogram)
   variance_b_max = 0
   q_max = -1
   n0 = 0
   n1 = 0
   
   for q in range(0, k - 2):
      n0 += histogram[q]
      n1 = MN - n0

      if (n0 > 0) and (n1 > 0):
         variance_b = (1 / (MN**2)) * n0 * n1 * ((mu0[int(q)] - mu1[int(q)])**2)

         if variance_b > variance_b_max:
            variance_b_max = variance_b
            q_max = q

   #image binarization
   for i in range(0, height):
      for j in range(0, width):
         if grayscale_image[i, j] <= q_max:
            binary_image[i, j] = 255
         else:
            binary_image[i, j] = 0

   return Image.fromarray(binary_image)      
   

def _make_mean_tables(histogram):
   k = len(histogram)
   mu0 = np.zeros(k)
   mu1 = np.zeros(k)
   n0, s0 = 0, 0

   for q in range(0, k):        
      n0 = n0 + histogram[q]
      s0 = s0 + (q * histogram[q])
      if n0 > 0:
         mu0[q] = s0 / n0
           
      else:
          mu0[q] = -1   

   N = n0
   n1, s1 = 0, 0
   mu1[k - 1] = 0
   
   for q in range(k - 2, 0, -1):
      n1 = n1 + histogram[q + 1]
      s1 = s1 + ((q + 1) * histogram[q + 1])
      if n1 > 0:
          mu1[int(q)] = s1 / n1
      else:
          mu1[int(q)] = -1

   return mu0, mu1, N   
