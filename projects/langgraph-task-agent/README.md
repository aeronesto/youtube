# Task Agent with LangGraph

This is a simple task agent that uses LangGraph to manage tasks.

## Prerequisites

- Install the [LangGraph CLI](https://langchain-ai.github.io/langgraph/cloud/reference/cli/).

```bash
pip install -U "langgraph-cli[inmem]"
```

# Deploy Application Locally

**Create Virtual Environment & Install dependencies**

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r my_agent/requirements.txt ## install dependencies from requirements.txt
```

## Deploy Redis and Postgres instances

Start up Redis and Postgres instances:

```bash
docker-compose up
``` 

## Build Application

Use the `langgraph build` command to build the application, instead of `docker build`:

```bash
langgraph build -t my-image
``` 

## Run Application

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

## Access Application

**Documentation**: http://localhost:8123/docs
**LangGraph Studio**: https://smith.langchain.com/studio/thread?baseUrl=http%3A%2F%2F127.0.0.1%3A8123

# Deploy Application in GCP