# Citibike Notebooks

## Setup

### Environment

I created an anaconda environment using the below command. The [conda docs](https://conda.io/docs/user-guide/tasks/manage-environments.html) provided for reference.

```shell
conda create --name venv python=3.5
```

Activating the environment:

```shell
activate venv
```

Deactivating the environment:

```shell
deactivate
```

### Packages 

Below are the commands I run to update/install Python packages for data analysis. The exclamation marks are special syntax for Jupyter Notebook to execute shell commands in a code cell. 

```
!pip install --upgrade --ignore-installed setuptools
!pip install --upgrade pandas
!pip install --upgrade google-api-python-client
!pip install --upgrade seaborn
!pip install pandas-gbq -U
```

The package pandas-gbq is for executing Google BigQuery queries (which create pandas DataFrames). For my specific case (Windows machine), I needed the --ignore-installed flag for setuptools to ensure that pandas-gbq is installed properly.

Below is for updating/installing scikit-learn. Note: you may need to restart the kernel to use certain modules like sklearn.model_selection.

```
!pip install -U scikit-learn
```

## Notes

The project_id variable is the ID of my Google Cloud project. This is necessary for using BigQuery as well as accessing my citibike_tripdata dataset.

```python
project_id = os.environ['project_id']
```