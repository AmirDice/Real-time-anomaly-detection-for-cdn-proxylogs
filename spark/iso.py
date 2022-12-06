#isolation forest
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
import os
import tempfile


if __name__ == "__main__":
        # Building a spark app/session
    spark = SparkSession.builder.appName("CDN_PROXY").getOrCreate()

# single cluster information
    df = spark.read.options(header='True', inferSchema='True', delimiter=',') \
.csv("./spark/data/cdata.csv")


    from pyspark_iforest.ml.iforest import *

    iforest = IForest(contamination=0.3, maxDepth=2)
    model = iforest.fit(df)

    model.hasSummary

    summary = model.summary

    summary.numAnomalies

    transformed = model.transform(df)

    rows = transformed.collect()

    temp_path = tempfile.mkdtemp()

    iforest_path = temp_path + "/iforest"

    iforest.save(iforest_path)

    loaded_iforest = IForest.load(iforest_path)

    model_path = temp_path + "/iforest_model"

    model.save(model_path)

    loaded_model = IForestModel.load(model_path)

    loaded_model.hasSummary

    loaded_model.transform(df).show()
    
spark.stop()