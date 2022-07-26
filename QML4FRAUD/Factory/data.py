import pandas as pd
import numpy as np
from pennylane import numpy as np
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

import pennylane as qml
#from pennylane_qiskit import IBMQDevice
#from pennylane_qiskit import BasicAerDevice
from pennylane.templates.embeddings import AngleEmbedding, AmplitudeEmbedding
from pennylane.optimize import AdamOptimizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

import time

class PrepareData:
    def __init__(self, data, target, sample_size = 0, test_split = 0.3, seed = 10):
        self.data = data
        self.preprocess_done = None
        
        if sample_size == 0:
            self.data_sample = data
        else:
            self.data_sample = data.sample(sample_size)
            
        self.train_set, self.test_set = train_test_split(self.data_sample, test_size=test_split, random_state=seed)
        
        self.y_train = self.train_set[[target]]
        self.y_test = self.test_set[[target]]
        
        self.x_train = self.train_set.drop(target, axis=1)
        self.x_test = self.test_set.drop(target, axis=1)
        
    def view_info(self):
        print(self.data_sample.info())
        if self.preprocess_done == None:
            print("No preprocessing done yet.")
        else:
            print("Preprocessing done via: ", self.preprocess_done)
        return self.data_sample.describe()
    
    def get_preprocessed(self, to_show = False):
        if self.preprocess_done == None:
            print("Please do some preprocessing first.")
        else:
            
            if to_show:
                print("Training Set and Labels: ")
                print(self.train_X_preprocessed)
                print(self.train_Y_preprocessed)

                print("Test Set and Labels: ")
                print(self.test_X_preprocessed)
                print(self.test_Y_preprocessed)
            
            return self.train_X_preprocessed, self.train_Y_preprocessed, self.test_X_preprocessed, self.test_Y_preprocessed
    
    def perform_LDA(self, n_dim = 2):
        
        self.preprocess_done = "LDA"
        print("Performing LDA...")
        
        length = len(self.x_train.columns)
        split_feature = int(length/n_dim)
        features_train = []
        features_test = []
        
        # Split Features (for Yaqi to change)
        for i in range(n_dim):
            new_set_train = self.x_train.iloc[:,(i*split_feature):((i+1)*split_feature)]
            features_train.append(new_set_train)
            
            new_set_test = self.x_test.iloc[:,(i*split_feature):((i+1)*split_feature)]
            features_test.append(new_set_test)
        
        # Run the LDA
        lda = LDA(n_components= (n_dim - 1))
        features_lda_train = []
        features_lda_test = []
        
        for i in range(n_dim):
            features_lda_train_new = lda.fit_transform(features_train[i], self.y_train)
            features_lda_train.append(pd.DataFrame(features_lda_train_new))
            
            features_lda_test_new = lda.fit_transform(features_test[i], self.y_test)
            features_lda_test.append(pd.DataFrame(features_lda_test_new))
        
        x_train_data = features_lda_train[0]
        x_test_data = features_lda_test[0]
        
        # Join the results together
        for i in range(1, n_dim):
            l_suffix = "_" + str(i)
            r_suffix = "_" + str(i+1)
            x_train_data = x_train_data.join(features_lda_train[i], lsuffix=l_suffix, rsuffix=r_suffix)
            x_test_data = x_test_data.join(features_lda_test[i], lsuffix=l_suffix, rsuffix=r_suffix)
        
        # Normalize
        std_scale_train = StandardScaler().fit(x_train_data)
        x_train_data = std_scale_train.transform(x_train_data)
        
        std_scale_test = StandardScaler().fit(x_test_data)
        x_test_data = std_scale_test.transform(x_test_data)
            
        # shift label from {0, 1} to {-1, 1}
        self.train_X_preprocessed = np.array(x_train_data, requires_grad=False)
        self.train_Y_preprocessed = np.array(self.y_train.values[:,0] * 2 - np.ones(len(self.y_train.values[:,0])), requires_grad = False)
        
        self.test_X_preprocessed = np.array(x_test_data, requires_grad=False)
        self.test_Y_preprocessed = np.array(self.y_test.values[:,0] * 2 - np.ones(len(self.y_test.values[:,0])), requires_grad = False)
        
    def perform_PCA(self, n_dim = 2):
        
        self.preprocess_done = "PCA"
        print("Performing PCA...")
        
        self.y_train.value_counts(normalize=True)*100
        self.y_test.value_counts(normalize=True)*100
        
        pca = PCA(n_components=n_dim, svd_solver='full')
        pca.fit(self.x_train)
        x_train_pca = pca.transform(self.x_train)
        pca.fit(self.x_test)
        x_test_pca = pca.transform(self.x_test)
        
        train_X_preprocessed = normalize(x_train_pca)
        test_X_preprocessed = normalize(x_test_pca)
        
        self.train_Y_preprocessed = np.array(self.y_train.values[:,0] * 2 - np.ones(len(self.y_train.values[:,0])), requires_grad = False)  # shift label from {0, 1} to {-1, 1}
        self.train_X_preprocessed = np.array(train_X_preprocessed, requires_grad=False)
        
        self.test_Y_preprocessed = np.array(self.y_test.values[:,0] * 2 - np.ones(len(self.y_test.values[:,0])), requires_grad = False)  # shift label from {0, 1} to {-1, 1}
        self.test_X_preprocessed = np.array(test_X_preprocessed, requires_grad=False)
        
    def perform_normalize(self, n_dim = 2):
        
        self.preprocess_done = "Normalize"
        print("Performing Normalize...")
        
        self.y_train.value_counts(normalize=True)*100
        self.y_test.value_counts(normalize=True)*100
        
        self.x_train.value_counts(normalize=True)*100
        self.x_test.value_counts(normalize=True)*100