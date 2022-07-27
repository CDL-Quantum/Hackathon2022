import pandas as pd
import numpy as np
import copy
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
        
        self.x_train = self.x_train.loc[:, self.x_train.any()]
        corr = self.x_train.corr()
        values_dont_change = corr.isnull().values
        for i in range(len(values_dont_change)):
            if values_dont_change[0][i]:
                index_to_drop = i
                self.x_train = self.x_train.drop(self.x_train.columns[index_to_drop], axis = 1)
        
    def view_info(self):
        print(self.x_train.info())
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
        group_columns = []
        df_clean_train_copy = copy.deepcopy(self.x_train)
        group_size = int(len(df_clean_train_copy.columns) / n_dim)
        
        for i in range(n_dim):
            corr_train = df_clean_train_copy.corr()

            max_value = 0
            for j in df_clean_train_copy.columns:
                #print(corr_train[j].abs().sort_values(ascending=False))
                if corr_train[j].abs().sort_values(ascending=False)[group_size - 1] >= max_value:
                    saved = j
                    max_value = corr_train[j].abs().sort_values(ascending=False)[group_size - 1]
            
            #print(saved)
            #print(max_value)
            #print(corr_train)
            #print(df_clean_train_copy.columns)
            #print(corr_train.columns)
            indices = corr_train[saved].abs().sort_values(ascending=False).index
            df_clean_train_copy = df_clean_train_copy[indices]
            new_columns = df_clean_train_copy.columns[:group_size]
            group_columns.append(new_columns)
            df_clean_train_copy = df_clean_train_copy.iloc[:, (group_size):]

        for i in range(n_dim):
            new_set_train = self.x_train[group_columns[i]]
            features_train.append(new_set_train)
            
            new_set_test = self.x_test[group_columns[i]]
            features_test.append(new_set_test)
        
        # Run the LDA
        features_lda_train = []
        features_lda_test = []
        LDA_transformations = []
        
        for i in range(n_dim):
            lda = LDA(n_components= (n_dim - 1))
            features_lda_train_new = lda.fit_transform(features_train[i], self.y_train)
            features_lda_train.append(pd.DataFrame(features_lda_train_new))
            LDA_transformations.append(lda)
            
            features_lda_test_new = lda.transform(features_test[i])
            features_lda_test.append(pd.DataFrame(features_lda_test_new))
        
        x_train_data = features_lda_train[0]
        x_test_data = features_lda_test[0]
        self.transformations = LDA_transformations
        
        # Join the results together
        for i in range(1, n_dim):
            l_suffix = "_" + str(i)
            r_suffix = "_" + str(i+1)
            x_train_data = x_train_data.join(features_lda_train[i], lsuffix=l_suffix, rsuffix=r_suffix)
            x_test_data = x_test_data.join(features_lda_test[i], lsuffix=l_suffix, rsuffix=r_suffix)
        
        # Normalize
        std_scale_train = StandardScaler().fit(x_train_data)
        x_train_data = std_scale_train.transform(x_train_data)
        
        x_test_data = std_scale_train.transform(x_test_data)
            
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
        x_test_pca = pca.transform(self.x_test)
        self.transformations = pca
        
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