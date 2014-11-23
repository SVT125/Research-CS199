import statistics
import math

def normpdf(x:float, mu:float, sigma:float) -> float:
    '''Calculates the normal PDF probability of x in a normal distribution N(mu,sigma).'''
    factor = 1/(sigma * (2*math.pi)**0.5)
    exponent = -0.5 * ((x-mu)/sigma) ** 2
    return factor * math.pow(math.e,exponent)

def anomalydetection(pos:str, threshold:float, examples:dict) -> bool:
    ''' Tests whether the pos'th example is an anomaly given the features of all examples. Declares anomaly if less than threshold.'''
    means, stddevs = [], []
    for key in range(len(examples.keys())):
        feature = retrieve_dict_vector(examples,key)
        means.append(statistics.mean(feature))
        stddevs.append(statistics.stdev(feature))

    probability = 1
    keys = examples.keys()
    feature_keys = keys[0].keys()
    for i in range(len(feature_keys)): # assumes means and stddevs have same length
        probability = probability * normpdf(features[pos][feature_keys[i]],means[i],stddevs[i])
    return probability < threshold

def optimize_threshold(labels:'list of bool',threshold:float, correctness:float, step_factor:float, examples:dict) -> float:
    '''Returns the optimized threshold given the example labels. Will assume
    decreasing values as partial derivatives can't easily be implemented without
    libraries for gradient descent.'''
    foundThreshold = False
    currentThreshold = threshold
    while not foundThreshold:
        correct = 0
        for i in range(len(features)):
            if labels[i] == anomalydetection(i,currentThreshold,examples):
                corrects += 1
        if corrects/len(labels) > correctness:
            foundThreshold = True
        currentThreshold = currentThreshold * step_factor
    return currentThreshold
'''
TEST CASES
#x,y,z the features of examples. Element 10 is designed anomalous.
x = [1,5,3,2,4,5,6,7,2,3,10]
y = [200,205,201,202,203,201,200,201,203,204,300]
z = [30,31,32,33,34,30,31,32,33,34,60]

# Detects the best threshold using scale factors - ideally, a different data set of (x,y,z) would be used.
threshold = optimize_threshold([False,False,False,False,False,False,False,False,False,True],1,0.2,0.1,
                               x,y,z)
'''
