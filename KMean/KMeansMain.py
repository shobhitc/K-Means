import random
from datetime import datetime
#import pandas as pd
#from pandas_confusion import ConfusionMatrix
import numpy as np
import time
import operator
import math
from _winapi import NULL
from pickle import INST

class KMeans:
    def __init__(self, file_name, attributes, target, k, max_iterations):
        self.file_name = file_name
        self.full_data = []
        self.training_data = []
        self.test_data = []
        self.attributes = attributes
        self.target = target
        self.separated_by_class = {}
        self.class_frequency = {}
        self.class_probability = {}
        self.features = {}
        self.total_training_instances = 0
        self.attrValDict = {}
        self.attrValList = {}
        self.classNumber = { 2 : "good" ,  3 : "vgood" ,  1 : "acc",    0 : "unacc" }
        self.max_iterations = max_iterations

        #self.binary_training_data = []
        self.binary_data = []
        self.k = k


    # runs the K Means Clustering
    def execute(self):
        self.read_file()
        self.readAttrList()
        self.convert_to_binary(self.full_data)
        #self.convert_to_binary(self.test_data, 'test')
        self.centroids = {}
        #initialize the centroids, the first 'k' elements in the dataset will be our initial centroids
        for i in range(self.k):
            rand=random.randint(0,1727)
            self.centroids[i] = self.binary_data[rand][0]
        self.checkResponse(self.binary_data)

        for i in range(self.max_iterations):
            self.classifications={}
            
            for i in range(self.k):
                self.classifications[i]=[]
                
            for x in range(len(self.binary_data)):
                distances=self.getDistance(self.binary_data[x], self.centroids, self.k)
                min = -1 
                classification = -1
                
                for index, p  in enumerate(distances):
                    if min == -1:
                        min = p
                        classification = index

                    else:
                        if min > p:
                            min = p
                            classification = index
                            
                        else:
                            next
                    
                
                self.classifications[classification].append(x)
            
            prev_centroids=dict(self.centroids)
            
            for classification in self.classifications:
                if(len(self.classifications[classification])!=0):
                    self.centroids[classification]=self.updateCenter(self.classifications[classification])
        
               
        for classification in self.classifications:
            self.getResponse(self.classifications[classification], classification)            
        
        
    def updateCenter(self, cluster_data):
        sum = [0]*24
        centroid = [0]*24
        for each in cluster_data:
            instance = self.binary_data[each][0]
            sum = [x + y for x, y in zip(sum, instance)]
    
        for index in range(len(sum)):
            if sum[index] == 0:
                centroid[index] = 0 
            else:
                centroid[index] = sum[index]/len(cluster_data)
            """list with values for centroid tuple""" 
        return centroid  

    def getDistance(self, binary_data, centroids, k):        
        distances = []
        length = len(centroids[0])
        for x in range(len(centroids)):
            dist = self.euclideanDistance(centroids[x], binary_data[0], length)
            #distances.append((binary_data, dist))
           
            distances.append((dist))
        
        #distances.sort(key=operator.itemgetter(1))
        return distances

    def checkResponse(self, classification):
        
        classVotes = {}
        classResponse = {}
        for x in range(len(classification)):
            
            response = self.binary_data[x][1]
            if response == [1, 0, 0, 0]:
                response = 'unacc'
            elif response == [0, 1, 0, 0]:
                response = 'acc'
            elif response == [0, 0, 1, 0]:
                response = 'good'
            elif response == [0, 0, 0, 1]:
                response = 'vgood'

            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
                
    def getResponse(self, classification, iteration):
        
        classVotes = {}
        classResponse = {}
        for x in range(len(classification)):
            response = self.binary_data[x][1]
            if response == [1, 0, 0, 0]:
                response = 'unacc'
            elif response == [0, 1, 0, 0]:
                response = 'acc'
            elif response == [0, 0, 1, 0]:
                response = 'good'
            elif response == [0, 0, 0, 1]:
                response = 'vgood'

            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
        #sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)

        maximum = max(classVotes, key=classVotes.get)
        error = len(classification) - classVotes[maximum];
        print('Cluster', iteration+1,":", len(self.classifications[iteration]), maximum)
        

    def getAccuracy(self, testSet, predictions):
        correct = 0
        for x in range(len(testSet)):
            if testSet[x][-1] == predictions[x]:
                correct += 1
        return (correct / float(len(testSet))) * 100.0





    def euclideanDistance(self, instance1, instance2, length):
        distance = 0

        for x in range(length):
            distance += pow((float(instance1[x]) - float(instance2[x])), 2)

        return math.sqrt(distance)


    # converts nominal data to binary data
    def convert_to_binary(self, data):
        # iterate through every instance
        for instance in data:
            # pass the instance to the helper function convert() which returns the instance as binary data
            self.binary_data.append(self.convert(instance))
            


    # helper function for convert_to_binary()
    def convert(self, instance):
        new_list = []
        final_list = []
        binary = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for i, attribute in enumerate(self.attributes):
            pos = self.attrValDict[attribute][instance[i]]
            binary[i][pos] = 1
        for i, each in enumerate(binary):
            if i < len(binary) - 1:
                new_list = new_list + each
            else:
                new_list = [int(x) for x in new_list]
                each = [int(x) for x in each]
                final_list.append(new_list)
                final_list.append(each)

        return final_list


    def readAttrList(self):
        with open("cardaten/attrList.txt", "r") as file:
            for line in file:
                line = line.strip("\r\n\t")
                key, val = (line.split(':'))
                val_list = val.split(",")
                new_list = {}
                self.attrValList[key] = val_list
                for i, l in enumerate(val_list):
                    new_list[l] = i
                self.attrValDict[key] = new_list


    def read_file(self):
        with open(self.file_name, "r") as file:
            for line in file:
                line = line.strip("\r\n")
                self.full_data.append(line.split(','))

        
        self.training_data = self.full_data



