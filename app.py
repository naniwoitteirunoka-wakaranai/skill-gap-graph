from fastapi import FastAPI
from pydantic import BaseModel
from graph.workflow import run_graph

app = FastAPI(title="Skill Gap Graph Service")


class GraphRequest(BaseModel):
    student: dict
    job: dict


@app.get("/health")
def health():
    return {"status": "graph-service-running"}


@app.post("/run")
def run(req: GraphRequest):
    return run_graph(req.student, req.job)