from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,FloatType,IntegerType
from pyspark.sql.functions import from_json,col

odometrySchema = StructType([
                StructField("id",IntegerType(),False),
                StructField("posex",FloatType(),False),
                StructField("posey",FloatType(),False),
                StructField("posez",FloatType(),False),
                StructField("orientx",FloatType(),False),
                StructField("orienty",FloatType(),False),
                StructField("orientz",FloatType(),False),
                StructField("orientw",FloatType(),False)
            ])

#  .config("spark.jars.packages","com.datastax.spark:spark-cassandra-connector_2.12:3.0.0")\
spark = SparkSession \
    .builder \
    .appName("SSKafka") \
    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "odometry") \
  .option("delimeter",",") \
  .option("startingOffsets", "latest") \
  .load() 

df.printSchema()

df1 = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"),odometrySchema).alias("data")).select("data.*")
df1.printSchema()


def writeToCassandra(writeDF, epochId):
  writeDF.write \
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="odometry", keyspace="ros")\
    .save()

df1.writeStream \
    .option("spark.cassandra.connection.host","localhost:9042")\
    .foreachBatch(writeToCassandra) \
    .outputMode("update") \
    .start()\
    .awaitTermination()
