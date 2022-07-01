CREATE EXTERNAL TABLE tweets (
   userid STRING,
   username STRING,
   acctdesc STRING,
   user_location STRING,
   user_following INT,
   user_followers INT,
   totaltweet INT,
   usercreated INT,
   tweetid BIGINT,
   tweetcreated INT,
   retweetco INT,
   texto STRING,
   hashtags array<STRUCT<textohashtag:STRING, indice:array<INT>>>, 
   language STRING,
   coordinate STRING,
   favorite_c INT,
   extractedts decimal(7, 0)
)
row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION '/topicosBD/tweets/';