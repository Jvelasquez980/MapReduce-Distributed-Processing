
# MapReduce-Distributed-Processing


## Authors

- [@Julian Osorio](https://github.com/julitZr)
- [@Jeronimo Velasquez](https://github.com/Jvelasquez980)
- [@Marcelo Castro](https://github.com/Eloven24)


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


Run this command

```bash
  python .\mapreduce\scripts\total_gdp_by_department.py .\data\data\cleaned_gdp_data.csv > .\mapreduce\results\output.txt 
```


## Data Documentation

[Documentation](https://linktodocumentation)


## Deployment

To deploy this project you need a aws account. Make a PUBLIC S3 bucket with 3 folders, logs, data and output(This one is not really necesary at this moment)
![image](https://github.com/user-attachments/assets/d38c4be1-9b57-4344-aae6-452d02820f1f)

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

Make a ssh conection to the master instance and upload the data/data/cleaned_gdp_data.csv and the mapreduce/scripts/total_gdp_by_department.py, after this run the next script data/scripts/cargar_hdfs.txt

```bash
  #!/bin/bash
# cargar_hdfs.sh

# Ruta local del archivo
LOCAL_FILE="cleaned_gdp_data.csv"
# Ruta destino en HDFS
HDFS_DIR="/user/hadoop/entrada"

# Crear carpeta si no existe
hdfs dfs -mkdir -p $HDFS_DIR

# Subir archivo
hdfs dfs -put -f $LOCAL_FILE $HDFS_DIR

# Verificar
hdfs dfs -ls $HDFS_DIR

python3 -m ensurepip --upgrade

pip3 install --user mrjob
```

Upload the files in hdfs and run the MapReduce with mapreduce/scripts/correr_map_reduce.txt

```bash
#!/bin/bash
#Modify S3_BUCKET to yours
# --- CONFIGURACIÓN ---
SCRIPT_PY="total_gdp_by_department.py"
INPUT_HDFS_PATH="hdfs:///user/hadoop/entrada/cleaned_gdp_data.csv"
OUTPUT_HDFS_DIR="hdfs:///user/hadoop/salida"
LOCAL_OUTPUT_FILE="resultados.csv"
S3_BUCKET="proyectotelematica"
S3_DEST_PATH="output/resultados.csv"

hdfs dfs -rm -r -f $OUTPUT_HDFS_DIR

python3 $SCRIPT_PY -r hadoop $INPUT_HDFS_PATH --output-dir $OUTPUT_HDFS_DIR

hdfs dfs -getmerge $OUTPUT_HDFS_DIR $LOCAL_OUTPUT_FILE

aws s3 cp $LOCAL_OUTPUT_FILE s3://$S3_BUCKET/$S3_DEST_PATH
```

Wait until the execution ends and check your S3 container, the output folder, if you didnt make it before would have been created, you must see the csv result

![image](https://github.com/user-attachments/assets/fbb4c929-f595-4298-8dc7-52da7cf68c94)

From the root folder of the S3 bucket, select the output folder and make it public
![image](https://github.com/user-attachments/assets/bebe78c3-6498-4f04-8f1d-bbbc117e0614)

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
