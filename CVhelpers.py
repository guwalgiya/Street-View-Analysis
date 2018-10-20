# ===============================================
# Import Packages and Functions
from   cv2               import addWeighted, bitwise_and, COLOR_BGR2HSV, cvtColor, inRange
import numpy             as     np
import matplotlib.pyplot as     plt

# ===============================================
# Function: whiteFilter
def colorFilter(input_image, colorFilter_para_bundle):
    
    # ===============================================
    # Load Parameters
    [gamma,        whiteFilter_para_bundle, yellowFilter_para_bundle] = colorFilter_para_bundle
    [lower_white,  upper_white,             white_weight]             = whiteFilter_para_bundle
    [lower_yellow, upper_yellow,            yellow_weight]            = yellowFilter_para_bundle
    
    
    # ===============================================
    # Parameters to array
    lower_white  = np.array(lower_white)
    upper_white  = np.array(upper_white)
    lower_yellow = np.array(lower_yellow)
    upper_yellow = np.array(upper_yellow)
    
    
    # ===============================================
    # Create Mask
    yellow_mask = inRange(input_image, lower_yellow, upper_yellow)
    white_mask  = inRange(input_image, lower_white,  upper_white)
    
    
    # ===============================================
    # Add Mask
    hsv_image    = cvtColor(input_image, COLOR_BGR2HSV)
    yellow_image = bitwise_and(hsv_image  , input_image, mask = yellow_mask)
    white_image  = bitwise_and(input_image, input_image, mask = white_mask)
    
    # ===============================================
    # Show Pictures
    plt.figure()
    plt.imshow(hsv_image)
    plt.figure()
    plt.imshow(yellow_image)
    plt.figure()
    plt.imshow(white_image)
    
    
    # ===============================================
    # Combine two masked picture
    image_out = addWeighted(white_image,  white_weight, 
                            yellow_image, yellow_weight,
                            gamma)
    
    # ===============================================
    return image_out