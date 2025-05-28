
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

Create the cluster and wait for 10 or 15 minutes. When the cluster





