# Task Agent with LangGraph

This README.md describes how to deploy a LangGraph agent on Google Cloud Platform.

The agent we are deploying is a simple task agent that uses LangGraph to manage tasks. This agent was described in Module 6 of the [Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) course in LangChain Academy. There are a few minor changes, including using Postgres as the checkpointer, instead of persisting in memory.


## Prerequisites

- Install the [LangGraph CLI](https://langchain-ai.github.io/langgraph/cloud/reference/cli/).

```bash
pip install -U langgraph-cli
```

## Deploy Application Locally

**Create Virtual Environment & Install dependencies**

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r my_agent/requirements.txt ### install dependencies from requirements.txt
```

#### Deploy Redis and Postgres instances

Start up Redis and Postgres instances:

```bash
docker-compose up
``` 

#### Build Application

Use the `langgraph build` command to build the application, instead of `docker build`:

```bash
langgraph build -t my-image
``` 

#### Run Application

Start up application, connecting it to the network (langgraph-task-agent_my_network) where the other services are running:

```bash
docker run \
    --network langgraph-task-agent_my_network \
    --env-file .env \
    -p 8123:8000 \
    -e DATABASE_URI=postgresql://user:pass@my_postgres:5432/mydb \
    -e REDIS_URI="redis://my_redis:6379" \
    my-image
```

#### Access Application

**Documentation**: http://localhost:8123/docs
**LangGraph Studio**: https://smith.langchain.com/studio/thread?baseUrl=http%3A%2F%2F127.0.0.1%3A8123

## Deploy Application in LangPlatform

LangGraph's [How to guide](https://langchain-ai.github.io/langgraph/how-tos/deploy-self-hosted/) to deploy to LangGraph Platform (formerly LangGraph Cloud)

## Deploy Application in Google Cloud Platform (GCP)

#### Create Virtual Private Cloud (VPC)

**Create a private network to be used by the application**

A VPC is required by Redis & Postgres to communicate within GCP.

[optional] If you need to access this network (i.e. from local machine), you'll need a jump host (a VM) to connect into the VPC.

#### Create Postgres Instance

Create a private Postgres instance to be used for persistence in your application (short & long-term memory) and run IDs

#### Create Redis Instance

Create Redis instance to be used to communicate between the HTTP worker and Queue worker in the LangGraph server

#### Create Cloud Build Config File

The `cloudbuild.yaml` file is where you:

* Build Docker image
* Save Docker image to Google Artifact Registry
* Provide environment variables to application
* Run the application on Cloud Run instance

Cloud Run is serverless, so we cannot connect it to the VPC directly. We will use a VPC connector to allow Cloud Run to access the private network where the Postgres instance resides.  This avoids exposing the database directly to the public internet.

#### Create VPC Connector

**A VPC Connector allows us to connect our serverless Cloud Run instance to the VPC.**

First we must create a subnet.

**[Create a subnet Documentation](https://cloud.google.com/sdk/gcloud/reference/compute/networks/subnets/create)**

CLI command to create a subnet:

`gcloud compute networks subnets create vpc-connector-subnet --network=default --range=10.10.0.0/28 --region=us-central1`

**[Create a VPC Connector Documentation](https://cloud.google.com/sdk/gcloud/reference/compute/networks/vpc-access/connectors/create)**

CLI command to create a VPC connector with a subnet:

`gcloud compute networks vpc-access connectors create task-maistro-vpc-con --region=us-central1 --subnet=vpc-connector-subnet`

Confirm the VPC connector was created:

`gcloud compute networks vpc-access connectors describe task-maistro-vpc-con --region=us-central1`

#### Create Cloud Build Trigger

set up cloud trigger when updates to github