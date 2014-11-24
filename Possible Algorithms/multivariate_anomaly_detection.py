from numpy import *
from scipy.stats import multivariate_normal
import math

def multivariate_anomaly_detection(pos:'str',threshold:float,examples:dict) -> bool:
        '''Determines whether the selected example in the dictionary, given by the key and threshold, is anomalous.'''
        '''Assume that the matrix passed for covariance is n x f, n = number of examples, f = features.'''
        x, y, z, mu = [], [], []
        for key in range(len(examples.keys())):
                feature = retrieve_dict_vector(examples,key)
                mu.append(statistics.mean(feature))
                covariances = cov(x,y,z)
        example = dict_to_list(examples[pos])
        return threshold > multivariate_normal(example,mu,covariances)
        
def retrieve_dict_vector(d:dict,key:str) -> list:
        '''Returns a list of all features across every example in d given a key.'''
        vector = []
        for example_key in d.keys():
                vector.append(d[example_key][key])
        return vector

def dict_to_list(d:dict) -> list:
        l = []
        for key in d.keys():
                l.append(d[key])
        return l



# Manual code
'''
        size = len(x)
        if size == len(mu) and (size, size) == sigma.shape:
                det = linalg.det(sigma)
        if det == 0:
        raise NameError("The covariance matrix can't be singular")

                norm_const = 1.0/ ( math.pow((2*pi),float(size)/2) * math.pow(det,1.0/2) )
                x_mu = matrix(x - mu)
                inv = sigma.I        
                result = math.pow(math.e, -0.5 * (x_mu * inv * x_mu.T))
                return norm_const * result
        else:
                raise NameError("The dimensions of the input don't match")
'''
