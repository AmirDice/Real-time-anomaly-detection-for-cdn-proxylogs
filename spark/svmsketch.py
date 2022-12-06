# SVM
from pyspark.ml.classification import LinearSVC
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from sklearn.model_selection import ParameterGrid
from pyspark.ml.tuning import CrossValidatior

lsvc = LinearSVC(maxIter=10)
if __name__ == "__main__":
    #elasticNetParam is regularization parameter, to prevent overfitting
    #fitIntercept is for weather we want to fit intercept for logistic or not
    spark = SparkSession.builder.appName("CDN_PROXY").getOrCreate()
    # single cluster information
    dataset = spark.read.options(header='True', inferSchema='True', delimiter=',') \
    .csv("./spark/data/cdata.csv")

    paramGrid = ParamGridBuilder() \
        .addGrid(lsvc.regParam, [0.1, 0.01]) \
        .addGrid(lsvc.fitIntercept, [False, True]) \
        .build()

    crossval = CrossValidator(estimator=lsvc,
                            estimatorParamMaps=paramGrid,
                            evaluator=BinaryClassificationEvaluator(),
                            numFolds=3)  # use 3+ folds in practice

    # Run cross-validation, and choose the best set of parameters.
    lsvc_cvModel = crossval.fit(dataset)

    

    # Compute predictions for test data
    predictions = lsvc_cvModel.bestModel.transform(dataset)

    # Show the computed predictions and compare with the original labels
    #predictions.select("features", "label", "prediction").show(10)

    # Define the evaluator method with the corresponding metric and compute the classification error on test data
    evaluator = MulticlassClassificationEvaluator().setMetricName('accuracy')
    #accuracy = evaluator.evaluate(predictions) 

    # Show the accuracy
    print("Intercept: " + str(lsvc_cvModel.bestModel.intercept))
    # print("Test accuracy = %g" % (accuracy))
    # print("Summary Stats")
    # print("Precision = %s" % precision)
    # print("Recall = %s" % recall)
    # #print("F1 Score = %s" % f1Score)
    spark.stop()