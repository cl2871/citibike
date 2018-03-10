

Jupyter Notebook Setup

# Install Gcloud SDK 

# (Create Dataproc Cluster)[https://cloud.google.com/dataproc/docs/guides/create-cluster#using_the_console_name]
 
> gcloud dataproc clusters create datascience --initialization-actions gs://dataproc-initialization-actions/jupyter/jupyter.sh

could use UI but must remember to add jupyter under initialization actions

# (SSH Tunneling and SOCKS)[https://cloud.google.com/dataproc/docs/concepts/accessing/cluster-web-interfaces]

> gcloud compute ssh --zone=master-host-zone master-host-name -- -D 1080 -N
note: get name of MASTER (e.g. datascience-m for datascience)

> "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --proxy-server="socks5://localhost:1080" --host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost" --user-data-dir=/tmp/master-host-name
note: run in another cli

connect to http://datascience-m:8088 #hadoop
connect to http://datascience-m:8123 #jupyter notebook

> !pip install pandas-gbq -U
# need this to run bigquery sql queries