# ===============================================
# Import Packages and Functions
import matplotlib.pyplot    as     plt
import numpy                as     np
from   sklearn.linear_model import LinearRegression
from   sklearn.mixture      import GMM
from   itertools            import combinations 
from   random               import sample

# ===============================================
# Use GMM to classify lines
def EM_Reg(train_data, num_cluster):
    
    
    # ===============================================
    # Initialization
    slopes    = sample(range(-100, 100), num_cluster)
    slopes    = [slope / 100 for slope in slopes]
    intercept = sample(range(-100, 100), num_cluster)
    
    for data_point in train_data:
        
    
    

      
    #return [pair[1] for pair in best_X1_all], [pair[1] for pair in best_X2_all], len(list(set(best_labels)))
