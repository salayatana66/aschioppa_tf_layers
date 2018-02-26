import tensorflow as tf
import numpy as np
import pandas as pd

class latentUnashedCategorical:
    numInstances = 0
    def __init__(self,categorical_values, default_index, key_type, num_latent_factors, prior_weights=None):
        latentUnashedCategorical.numInstances += 1
        self.lookupDataFrame = pd.DataFrame({"values" : categorical_values,
                                        "indices" : np.array(xrange(len(categorical_values)))
                                        })
        self.default_index = default_index
        self.num_latent_factors = num_latent_factors

        self.lookupTable = tf.contrib.lookup.HashTable(
                 tf.contrib.lookup.KeyValueTensorInitializer(self.lookupDataFrame.values.values,
                                                             self.lookupDataFrame.indices.values,
                    key_dtype=key_type,value_dtype=tf.int64),
                    default_value = self.default_index)
        self.inverseLookupTable=tf.contrib.lookup.HashTable(
                 tf.contrib.lookup.KeyValueTensorInitializer(self.lookupDataFrame.indices.value,
                                                             self.lookupDataFrame.values.values,

                    key_dtype=tf.int64,value_dtype=key_type),
                    default_value = categorical_values[self.default_index])
        if prior_weights is None:
            self.weights = tf.get_variable(name="latentUnashedCategoricalWeights"+
                                           str(latentUnashedCategorical.numInstances),
                                           shape = [len(categorical_values),
                                                       self.num_latent_factors],
                                              initializer =
                                              tf.truncated_normal_initializer(
                                                  mean = 0.0,
                                                  stddev=1.0/np.sqrt(self.num_latent_factors),
                                                  dtype=tf.float64),dtype=tf.float64)
        else:
            self.weights = tf.get_variable(name="latentUnashedCategoricalWeights"+
                                           str(latentUnashedCategorical.numInstances),
                                               initializer =
                                              tf.constant(value=prior_weights,
                                                          dtype=tf.float64),
                                               dtype=tf.float64)


    def getLookupLayer(self, inputTensor):
        return self.lookupTable.lookup(inputTensor)

    def getInverseLookupLayer(self, inputTensor):
        return self.inverseLookupTable.lookup(inputTensor)

    def getLatentLayer(self, inputTensor, withLookup = True):
        if withLookup:
            return tf.nn.embedding_lookup(self.weights, self.lookupTable.lookup(inputTensor))
        else:
            return tf.nn.embedding_lookup(self.weights, inputTensor)

    def getAsDict(self, Session):
        return {"lookupDataFrame" : self.lookupDataFrame,
                    "weights" : Session.run(self.weights),
                    "num_latent_factors" : self.num_latent_factors
        }





