
# MapReduce-Distributed-Processing


## Authors

- [@Julian Osorio](https://github.com/julitZr)
- [@Jeronimo Velasquez](https://github.com/Jvelasquez980)
- [@Marcelo Castro](https://github.com/Eloven24)

## Data Documentation

[Data Documentation](https://github.com/Jvelasquez980/MapReduce-Distributed-Processing/wiki/Data-documentation)

## Features Docs

[Features Documentation](https://github.com/Jvelasquez980/MapReduce-Distributed-Processing/wiki/Features)

## Run Locally

Clone the project

```bash
  git clone https://github.com/Jvelasquez980/MapReduce-Distributed-Processing.git
```

Go to the project directory

```bash
  cd MapReduce-Distributed-Processing
```

Install requirements

```bash
# You could use a virtual Enviroment
# You must use python 3.11, mrjob doesnt work well with a different python version
  pip install -r requirements.txt
```
Get the data
```python
python.exe .\data\scripts\getData.py
```


Run the map reduce

```bash
  python .\mapreduce\scripts\total_gdp_by_department.py .\data\data\cleaned_gdp_data.csv > .\mapreduce\results\output.csv
```
You can visualize the map reduce result in mapreduce\results\output.csv




## Deployment

To deploy this project you need a aws account. Make a PUBLIC S3 bucket with 5 folders, logs, data, scripts, input and output, upload the mapreduce/scripts/total_gdp_by_department.py in scripts folder and the data/data/cleaned_gdp_data.csv in input folder.
![image](https://github.com/user-attachments/assets/d2fef93b-5b60-42d1-918f-6486e9a6695b)
![image](https://github.com/user-attachments/assets/4708477c-c47a-486b-aab7-2de5bef1d9fd)
![image](https://github.com/user-attachments/assets/a412d8bb-6e71-4a80-b81f-64266940d50e)



After this you need to run an EMR cluster instance, with this applications already installed
![image](https://github.com/user-attachments/assets/e9423b78-1778-46cc-94f8-15b9bfa05410)
![image](https://github.com/user-attachments/assets/18b1e8c7-e7bf-47d3-b338-2be0955b4694)

In cluster configuration select Uniform instance groups, and in all the storage of the 3 different instances (Master, and the 2 slaves), select m4.large

![image](https://github.com/user-attachments/assets/f7aa5148-9dd4-403d-a4ea-4c58f551dc61)

In Cluster termination and node replacement, you could modify the time where the cluster is up
![image](https://github.com/user-attachments/assets/4979b167-a39e-4bb2-919d-b58cd621f96e)

In cluster logs search the bucket that you already create, and put the logs folder direction
![image](https://github.com/user-attachments/assets/94948547-478d-4f43-88da-28e8df8cb9da)

In Security configuration and EC2 key pair, select a create and select a key pair. In the last part, Identity and Access Management (IAM) roles select all default roles

![image](https://github.com/user-attachments/assets/f669cd6e-fda5-4fcd-861f-f54e900ebfa5)

Create the cluster and wait for 10 or 15 minutes. When the cluster status says "waiting"
![image](https://github.com/user-attachments/assets/25c34255-6e24-4ec9-99c9-f8cf7f279a62)

Change the inbound rules from the security group of the master instance and add and ssh rule
![image](https://github.com/user-attachments/assets/2edb5824-bdb8-47fc-8917-dc126051245b)

Make a ssh conection to the master and run the next script data/scripts/cargar_hdfs.txt

```bash
#!/bin/bash
# cargar_hdfs.sh

# --- CONFIGURACIÓN ---
# USE YOUR OWN BUCKET
BUCKET="proyectotelematica"
OBJECT_KEY="input/cleaned_gdp_data.csv"
LOCAL_FILE="cleaned_gdp_data.csv"
HDFS_DIR="/user/hadoop/entrada"

# 1. Descargar archivo desde S3

aws s3 cp s3://$BUCKET/$OBJECT_KEY $LOCAL_FILE

# 2. Crear carpeta en HDFS si no existe

hdfs dfs -mkdir -p $HDFS_DIR

# 3. Subir archivo a HDFS

hdfs dfs -put -f $LOCAL_FILE $HDFS_DIR

# 4. Verificar subida

hdfs dfs -ls $HDFS_DIR

# 5. Instalar mrjob si es necesario

python3 -m ensurepip --upgrade
pip3 install --user mrjob

```

Upload the files in hdfs and run the MapReduce with mapreduce/scripts/correr_map_reduce.txt

```bash
#!/bin/bash

# --- CONFIGURACIÓN ---
S3_BUCKET="proyectotelematica"
SCRIPT_KEY="scripts/total_gdp_by_department.py"
SCRIPT_PY="total_gdp_by_department.py"

INPUT_HDFS_PATH="hdfs:///user/hadoop/entrada/cleaned_gdp_data.csv"
OUTPUT_HDFS_DIR="hdfs:///user/hadoop/salida"
LOCAL_OUTPUT_FILE="resultados.csv"
S3_DEST_PATH="output/resultados.csv"

# Descargar el script desde S3
if ! aws s3 cp s3://$S3_BUCKET/$SCRIPT_KEY $SCRIPT_PY; then
    exit 1
fi

# Eliminar salida anterior en HDFS
hdfs dfs -rm -r -f $OUTPUT_HDFS_DIR

# Ejecutar MapReduce
python3 $SCRIPT_PY -r hadoop $INPUT_HDFS_PATH --output-dir $OUTPUT_HDFS_DIR

# Unificar resultados
hdfs dfs -getmerge $OUTPUT_HDFS_DIR $LOCAL_OUTPUT_FILE

# Subir resultado final a S3
aws s3 cp $LOCAL_OUTPUT_FILE s3://$S3_BUCKET/$S3_DEST_PATH


```

Wait until the execution ends and check your S3 container, the output folder, if you didnt make it before would have been created, you must see the csv result

![image](https://github.com/user-attachments/assets/fbb4c929-f595-4298-8dc7-52da7cf68c94)

From the root folder of the S3 bucket, select the output folder and make it public

![image](https://github.com/user-attachments/assets/7f7ba167-a395-42c2-aac3-3f0baea22d53)


Now you have 2 options, run the api locally changing S3_URL = "https://proyectotelematica.s3.us-east-1.amazonaws.com/output/resultados.csv" for yours
```python
from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)
S3_URL = "https://YOURS/output/resultados.csv"
```
And running it locally with "python .\mapreduce\API\app.py" or since API folder just run the docker-compose with docker-compose up -d , you should see in your browser from this url http://192.168.1.25:5000/api/resultados
![image](https://github.com/user-attachments/assets/c26e23bb-e2ac-412a-9f36-ca39a18b4855)

If you want to have the api deployed too, jut create a EC2 instance, allow the tcp traffic to port 5000, make the ssh connection and upload the API folder, install docker in the instance with
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

Run 
```bash
cd API
docker-compose up -d
```
You should see since the ip of the EC2 instace the same as you saw locally.

Also as an extra we made a web application to have a better visualization of the data. As the api, you can decide if you want to make it public (In a AWS EC2 instance) or you can run ut locally. If you decided to run it locally download the requirements in web_visualizer/requirements.txt with 
```bash
pip install -r web_visualizer/requirements.txt
```
After this you can change the port of execution to one different of 5000, this because the api use the same port and if you run it both locally you will have some problems. At the end. To visualize it change this from web_visualizer/visual_app.py

```python
app = Flask(__name__)
DATA_URL = "http://174.129.242.86:5000/api/resultados" #After
DATA_URL = "http://localhost:5000/api/resultados" #Before
#Use the ip of the instance that you made and the port where you were running the api
```
Run the aplication and you will see the final result
![image](https://github.com/user-attachments/assets/46cb8141-88bc-48dd-88b0-e8edfde5eb47)

If you decide to made a EC2 instance just upload the folder web_visualizer in the instance an run 
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo usermod -aG docker $USER
cd web_visualizer/
sudo docker-compose up -d
```
This will launch the application in docker container, and will be running in the port 5000 so make sure that you activate this port in the security groups

