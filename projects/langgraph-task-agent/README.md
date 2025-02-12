# Task Agent with LangGraph

This is a simple task agent that uses LangGraph to manage tasks.

## Prerequisites

- Install the [LangGraph CLI](https://langchain-ai.github.io/langgraph/cloud/reference/cli/).

## Build Application

Use the `langgraph build` command to build the application, instead of `docker build`:

```bash
langgraph build -t my-image
``` 

## Run application

Run the application individually, connecting it to the network (task_maistro_app_my_network) where the other services are running:

```bash
docker run \
    --network task_maistro_app_my_network \
    --env-file .env \
    -p 8123:8000 \
    -e DATABASE_URI=postgresql://user:pass@my_postgres:5432/mydb \
    -e REDIS_URI="redis://my_redis:6379" \
    my-image
```