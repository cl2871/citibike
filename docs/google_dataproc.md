# Analysis Using Google Dataproc

## Jupyter Notebook Setup

Google offers Apache Spark clusters through its Dataproc service, and I utilize this to present results and visualizations using a Jupyter Notebook. 

### [Install Google Cloud SDK](https://cloud.google.com/sdk/) 

The SDK provides command line access to Google's services.

```Shell
gcloud init
```

### Create Dataproc Cluster

A cluster called datascience will be spun up using the below code. It will have Jupyter Notebook installed.

```Shell
gcloud dataproc clusters create datascience --initialization-actions gs://dataproc-initialization-actions/jupyter/jupyter.sh
```

You could do the same thing on the [user interface](https://cloud.google.com/dataproc/docs/guides/create-cluster#using_the_console_name) but remember to add the jupyter path under initialization actions.

### [SSH Tunneling and SOCKS](https://cloud.google.com/dataproc/docs/concepts/accessing/cluster-web-interfaces)

Have 2 command line interfaces open. One will be for the SSH tunnel and the other will be for starting a browser session with SOCKS proxy settings (see link above for more info). 


SSH Tunnel:

```Shell
gcloud compute ssh --zone=master-host-zone master-host-name -- -D 1080 -N
```
Notes: 
- use name of MASTER node (e.g. datascience-m for datascience)
- need Putty for Windows

SOCKS Proxy Session:

```Shell
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --proxy-server="socks5://localhost:1080" --host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost" --user-data-dir=/tmp/master-host-name
```

### Connecting to Dataproc Cluster

Using the browser opened with SOCKS proxy settings, you can directly connect to the cluster services via the below URLs (hadoop and jupyter notebook respectively).

http://datascience-m:8088
http://datascience-m:8123 

After connecting to the second URL, you can create a PySpark notebook and run Python commands.

Install libraries:

```
!pip install --upgrade pandas
!pip install --upgrade google-api-python-client
!pip install --upgrade seaborn
!pip install pandas-gbq -U
```

### Cleanup

Save the notebook and download it when finished. Run the below command to shut down the cluster to save money. 

```Shell
gcloud dataproc clusters delete datascience
```
