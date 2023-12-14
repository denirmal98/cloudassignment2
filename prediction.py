from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.sql.session import SparkSession

def create_spark_session(app_name):
    """
    Create a Spark session with the given app name.
    """
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    configure_s3_settings(spark)
    return spark

def configure_s3_settings(spark):
    """
    Configure Spark session for S3 access.
    """
    spark.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider",
                                     "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.AbstractFileSystem.s3a.impl", "org.apache.hadoop.fs.s3a.S3A")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", "ASIAQE4M2SYIZRZ3C7EN")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "vsLYkGNPklMGzuMGYk/X9O6y9GdWWRIOcMuro5wH")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")

def load_validation_data(spark, s3_path):
    """
    Load validation data from the specified S3 path.
    """
    validation_df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("sep", ";") \
        .load(s3_path)

    if validation_df.count() > 0:
        print("Data loaded successfully")
    else:
        print("Something unexpected happened during data load")

    return validation_df

def rename_columns(validation_df, column_mapping):
    """
    Rename columns in the DataFrame based on the provided mapping.
    """
    for current_name, new_name in column_mapping.items():
        validation_df = validation_df.withColumnRenamed(current_name, new_name)
    return validation_df

def evaluate_model(model, validation_df, evaluator):
    """
    Evaluate the model on the validation data and print the F1 score.
    """
    print("F1 Score for Model: ", evaluator.evaluate(model.transform(validation_df)))

if __name__ == "__main__":
    # Set your unique app name
    app_name = "CS643_Wine_Quality_Predictions_Project"

    # Create Spark session
    spark_session = create_spark_session(app_name)

    # Load validation data from S3
    s3_validation_path = "s3a://mldatawineprediction/ValidationDataset.csv"
    validation_data = load_validation_data(spark_session, s3_validation_path)

    # Define column name mapping
    column_name_mapping = {
        '"""""fixed acidity""""': 'fixed_acidity',
        '"""fixed acidity""""': 'fixed_acidity',
        '""""volatile acidity""""': 'volatile_acidity',
        '""""citric acid""""': 'citric_acid',
        '""""residual sugar""""': 'residual_sugar',
        '""""chlorides""""': 'chlorides',
        '""""free sulfur dioxide""""': 'free_sulfur_dioxide',
        '""""total sulfur dioxide""""': 'total_sulfur_dioxide',
        '""""density""""': 'density',
        '""""pH""""': 'pH',
        '""""sulphates""""': 'sulphates',
        '""""alcohol""""': 'alcohol',
        '""""quality"""""': 'label'
    }

    # Rename columns in the DataFrame
    validation_data = rename_columns(validation_data, column_name_mapping)

    # Load the pre-trained model
    model_path = "s3a://mldatawineprediction/LogisticRegression"
    trained_model = CrossValidatorModel.load(model_path)

    # Create a MulticlassClassificationEvaluator
    classification_evaluator = MulticlassClassificationEvaluator(metricName="f1")

    # Evaluate the model on validation data and print F1 score
    evaluate_model(trained_model, validation_data, classification_evaluator)
