# ===============================================
# Import Packages and Functions
from   moviepy.editor    import VideoFileClip
from   processImages     import processImage
from   snipper           import scope
from   painter           import draw, mixing
from   os                import remove
import matplotlib.pyplot as     plt
import matplotlib.image  as     mpimg
import numpy             as     np


# ===============================================
# Changeable Operating System Parameters
slash = "\\"


# ===============================================
# Changeable Database Parameters
image_folder        = "C:\\Street-View-Analysis\\Data"
original_image_name = "solidWhiteRight.jpg"
output_image_name   = ""
video_folder        = "C:\\Street-View-Analysis\\Data"
input_video_name    = "solidWhiteRight.mp4"
output_video_name   = "white.mp4"


# ===============================================
# Changeable Process Parameters
blur_kernel_size = 1
sigma_X          = 0
low_threshold    = 100
high_threshold   = 150
lower_white      = [155, 155, 155] #160 160 160
upper_white      = [255, 255, 255]
lower_yellow     = [90,  100, 100]
upper_yellow     = [110, 255, 255]
white_weight     = 1
yellow_weight    = 0
gamma            = 0


# ===============================================
# Target Region Parameters
trap_bottom_width = 1     # 0.85
trap_top_width    = 0.3     # 0.7
trap_height       = 0.34   # 0.4
mask_color        = 255  
if_show_region    = False


# ===============================================
# Hough Transform
if_show_R_cluster = False
if_show_L_cluster = False
if_show_scatters  = False
if_show_fit_lines = False
min_line_length   = 5     # 10
slope_threshold   = 0
painting_color    = (255, 255, 0)
max_line_gap      = 5
line_channel      = 3
theta_degree      = 1
draw_height       = 0.65
threshold         = 15
data_type         = np.uint8
thick             = 10
rho               = 3


# ===============================================
# Arrange Mixer Parameters
mixer_gamma           = 0
line_image_weight     = 1   
original_image_weight = 1


# ===============================================
# Top Level
if_show_original_image = False
if_show_target_region  = False
if_show_final_image    = False


# ===============================================
# Integrate Database Parameters
original_image_path = image_folder + slash + original_image_name


# ===============================================
# Integrate Processing Parameters 
blur_kernel = (blur_kernel_size, blur_kernel_size)


# ===============================================
# Integrate Drawing Parameters
theta_radius = theta_degree * np.pi / 180


# ===============================================
# Arrange all Parameters - Ground Floor - Blur_Parameters
blur_para_bundle            = {}
blur_para_bundle["kernel"]  = blur_kernel
blur_para_bundle["sigma_X"] = sigma_X


# ===============================================
# Arrange all Parameters - Ground Floor
canny_para_bundle        = {}
canny_para_bundle["l_t"] = low_threshold
canny_para_bundle["h_t"] = high_threshold


# ===============================================
# Arrange all Parameters - Ground Floor
whiteFilter_para_bundle           = {}
whiteFilter_para_bundle["low"]    = lower_white
whiteFilter_para_bundle["high"]   = upper_white
whiteFilter_para_bundle["weight"] = white_weight


# ===============================================
# Arrange all Parameters - Ground Floor
yellowFilter_para_bundle           = {}
yellowFilter_para_bundle["low"]    = lower_yellow
yellowFilter_para_bundle["high"]   = upper_yellow
yellowFilter_para_bundle["weight"] = yellow_weight


# ===============================================
# Arrange all Parameters - Second Floor
colorFilter_para_bundle           = {}
colorFilter_para_bundle["gamma"]  = gamma
colorFilter_para_bundle["white"]  = whiteFilter_para_bundle
colorFilter_para_bundle["yellow"] = yellowFilter_para_bundle


# ===============================================
# Arrange all Parameters - Top Level
process_parameters_bundle           = {}
process_parameters_bundle["blur"]   = blur_para_bundle
process_parameters_bundle["canny"]  = canny_para_bundle
process_parameters_bundle["filter"] = colorFilter_para_bundle


# ===============================================
# Arrange all Parameters - Top Level
vertices_parameters_bundle                   = {}
vertices_parameters_bundle["m_color"]        = mask_color
vertices_parameters_bundle["t_height"]       = trap_height
vertices_parameters_bundle["t_twidth"]       = trap_top_width
vertices_parameters_bundle["t_bwidth"]       = trap_bottom_width
vertices_parameters_bundle["thickness"]      = thick
vertices_parameters_bundle["if_show_region"] = if_show_region


# ===============================================
# Arrange Painter Parameters
draw_parameters_bundle                      = {}
draw_parameters_bundle["if_show_R_cluster"] = if_show_R_cluster
draw_parameters_bundle["if_show_L_cluster"] = if_show_L_cluster
draw_parameters_bundle["if_show_scatters"]  = if_show_scatters
draw_parameters_bundle["draw_height"]       = draw_height
draw_parameters_bundle["h_threshold"]       = threshold
draw_parameters_bundle["s_threshold"]       = slope_threshold
draw_parameters_bundle["min_len"]           = min_line_length
draw_parameters_bundle["max_gap"]           = max_line_gap
draw_parameters_bundle["channel"]           = line_channel
draw_parameters_bundle["d_type"]            = data_type 
draw_parameters_bundle["color"]             = painting_color
draw_parameters_bundle["theta"]             = theta_radius
draw_parameters_bundle["thick"]             = thick
draw_parameters_bundle["rho"]               = rho


# ===============================================
# Arrange Mixer Parameters
mixing_para_bundle                          = {}
mixing_para_bundle["mixer_gamma"]           = mixer_gamma
mixing_para_bundle["line_image_weight"]     = line_image_weight     
mixing_para_bundle["original_image_weight"] = original_image_weight 


# ===============================================
# Prepare I
initial_data_array = np.array([])
initial_data_array = initial_data_array.reshape((len(initial_data_array), 2))


# ===============================================
# Prepare II
dict_empty = {}
for i in range(12):
    dict_empty[-i] = initial_data_array
np.save("train_data_L.npy", dict_empty)
np.save("train_data_R.npy", dict_empty)


# ===============================================
# Load Image
original_image = mpimg.imread(original_image_path)

if if_show_original_image:
    plt.figure()
    plt.imshow(original_image)


# ===============================================
# Process Image
processed_image = processImage(original_image, process_parameters_bundle)


# ===============================================
# Find traget region
target_region = scope(original_image, processed_image, vertices_parameters_bundle)



# ===============================================
# Draw Lines
line_image = draw(original_image, target_region, draw_parameters_bundle)
if if_show_original_image:
    plt.figure()
    plt.imshow(line_image)

# ===============================================
# Combine
final_image = mixing(original_image, line_image, mixing_para_bundle)
if if_show_final_image:
    plt.figure()
    plt.imshow(final_image)


# ===============================================
# this function is used to work on videos
def ensemble(input_image):
    processed_image = processImage(input_image, process_parameters_bundle)
    target_region   = scope(input_image, processed_image, vertices_parameters_bundle)
    line_image      = draw(original_image, target_region, draw_parameters_bundle)
    final_image     = mixing(input_image, line_image, mixing_para_bundle)
    return final_image


# =============================================== 
# Call function ENSEMBLE to perform lane detection on a short video
input_clip  = VideoFileClip(video_folder + slash + input_video_name)
output_clip = input_clip.fl_image(ensemble) 
output_clip.write_videofile(output_video_name, audio = False, verbose = False)


# =============================================== 
# Clean Temp File
remove("train_data_L.npy")
remove("train_data_R.npy")