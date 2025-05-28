
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

To deploy this project you need a aws account, you need a emr cluster 


