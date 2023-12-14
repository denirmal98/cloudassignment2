from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml import Pipeline
from pyspark.sql.functions import col, isnan

def create_spark_session():
    """
    Create and configure a Spark session.
    """
    spark = SparkSession.builder \
        .master("local") \
        .appName("CS643_Wine_Quality_Predictions_Project") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.2") \
        .getOrCreate()

    configure_s3_access(spark)

    return spark

def configure_s3_access(spark):
    """
    Configure S3 access for Spark session.
    """
    spark.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", \
                                                      "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.AbstractFileSystem.s3a.impl", "org.apache.hadoop.fs.s3a.S3A")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", "ASIAQE4M2SYIZRZ3C7EN")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "vsLYkGNPklMGzuMGYk/X9O6y9GdWWRIOcMuro5wH")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")

def load_data(spark, train_path, validation_path):
    """
    Load training and validation datasets.
    """
    df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("sep", ";") \
        .load(train_path)

    validation_df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("sep", ";") \
        .load(validation_path)

    return df, validation_df

def check_data_loaded(df, validation_df):
    """
    Check if data is loaded successfully.
    """
    if df.count() > 0 and validation_df.count() > 0:
        print("Data loaded successfully")
    else:
        print("Something unexpected happened during data load")

def rename_columns(df, validation_df):
    """
    Rename columns in the DataFrames.
    """
    new_column_names = {
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

    for current_name, new_name in new_column_names.items():
        df = df.withColumnRenamed(current_name, new_name)
        validation_df = validation_df.withColumnRenamed(current_name, new_name)

    return df, validation_df

def print_null_counts(df):
    """
    Print null or NaN counts for each column in the DataFrame.
    """
    null_counts = []
    for col_name in df.columns:
        null_count = df.filter(col(col_name).isNull() | isnan(col(col_name))).count()
        null_counts.append((col_name, null_count))

    for col_name, null_count in null_counts:
        print(f"Column '{col_name}' has {null_count} null or NaN values.")

def split_data(df):
    """
    Split the DataFrame into training and test sets.
    """
    train_df, test_df = df.randomSplit([0.7, 0.3], seed=42)
    return train_df, test_df

def build_pipeline(model):
    """
    Build a ML pipeline with vector assembler, scaler, and the specified model.
    """
    assembler = VectorAssembler(
        inputCols=['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides',
                   'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol'],
        outputCol="inputFeatures")

    scaler = StandardScaler(inputCol="inputFeatures", outputCol="features")

    pipeline = Pipeline(stages=[assembler, scaler, model])

    return pipeline

def train_and_evaluate_model(pipeline, train_df, test_df, evaluator):
    """
    Train and evaluate the model using cross-validation.
    """
    param_grid = ParamGridBuilder().build()

    crossval = CrossValidator(estimator=pipeline,
                              estimatorParamMaps=param_grid,
                              evaluator=evaluator,
                              numFolds=10)

    cv_model = crossval.fit(train_df)

    print("F1 Score for the model: ", evaluator.evaluate(cv_model.transform(test_df)))

    return cv_model

def save_model(cv_model, model_path):
    """
    Save the trained model to the specified path.
    """
    cv_model.save(model_path)

def main():
    # Define paths for training and validation datasets
    train_data_path = "s3a://mldatawineprediction/TrainingDataset.csv"
    validation_data_path = "s3a://mldatawineprediction/ValidationDataset.csv"

    # Create Spark session
    spark = create_spark_session()

    # Load training and validation datasets
    df, validation_df = load_data(spark, train_data_path, validation_data_path)

    # Check if data is loaded successfully
    check_data_loaded(df, validation_df)

    # Rename columns in the DataFrames
    df, validation_df = rename_columns(df, validation_df)

    # Print null or NaN counts for each column
    print_null_counts(df)

    # Split the DataFrame into training and test sets
    train_df, test_df = split_data(df)

    # Build a ML pipeline with Logistic Regression model
    logistic_regression_model = LogisticRegression()
    logistic_regression_pipeline = build_pipeline(logistic_regression_model)
