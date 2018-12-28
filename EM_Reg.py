# ===============================================
# Import Packages and Functions
import matplotlib.pyplot    as     plt
import numpy                as     np
from   sklearn.linear_model import LinearRegression
from   sklearn.mixture      import GMM
from   itertools            import combinations 
from   random               import sample, randint


# ===============================================
# Use GMM to classify lines
# def EM_Reg(train_data, num_cluster):
    
train_data = np.load("dabug_data_1.npy")
num_cluster = 3
slope_bound = 100
sigma       = 0.5
# ===============================================
# Initialization
slopes     = sample(range(-1 * slope_bound, slope_bound), num_cluster)
slopes     = [slope / slope_bound for slope in slopes]
intercepts = sample(range(-1 * slope_bound, slope_bound), num_cluster)
#intercepts = [intercept / slope_bound for intercept in intercepts]
#intercept = [0] * num_cluster
labels = np.array([randint(0, num_cluster - 1) for data_point in train_data])
print(labels)
#labels = [0] * len(train_data)
itr = 1


while itr < 4:
    if True:
        plt.figure()
        plt.axis([0, 540, 0, 540])
        plt.scatter(train_data[:, 0], train_data[:, 1], c = labels, cmap= "viridis")
        plt.gca().invert_yaxis()  
        
    try:    
        for label in range(num_cluster):
            indices  = np.where(labels == label)[0].tolist()
            reg_data = train_data[indices]
            reg      = LinearRegression().fit(reg_data[:, 0].reshape(-1, 1), reg_data[:, 1])
            k = reg.coef_[0]
            b = reg.intercept_
            slopes[label]     = k
            intercepts[label] = b
            y_pred = reg.predict(reg_data[:, 0].reshape(-1, 1))
            plt.plot(reg_data[:, 0], y_pred, color = 'red', linewidth = 1)
    except:
        pass    

        
    for i in range(len(train_data)):
        x        = train_data[i][0] 
        y        = train_data[i][1] 
        perpen_x = np.divide((np.multiply(slopes, x) - intercepts + y), 
                              np.multiply(slopes, 2))
        perpen_y = np.divide((np.multiply(slopes, x) + intercepts + y), 2)
        distance = np.sqrt(np.power(x - perpen_x, 2) + np.power(y - perpen_y, 2))
        
        #residual = np.abs(np.multiply(slopes, x) + intercepts - y)
        #exp_residual = np.exp(-1 * np.power(residual, 2) / (2 * np.power(sigma, 2)))
        #eights  = np.divide(exp_residual, sum(exp_residual))
        #weights = np.divide(residual, sum(residual))
        #labels[i] = np.argmax(residual)
        labels[i]  = np.argmin(distance)

    itr = itr + 1