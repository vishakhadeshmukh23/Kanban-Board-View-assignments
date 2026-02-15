from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dag_utils import is_dag_dfs, find_cycle_dfs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

class PipelineEdge(BaseModel):
    source: str
    target: str


class PipelineNode(BaseModel):
    id: str


class PipelinePayload(BaseModel):
    nodes: List[PipelineNode]
    edges: List[PipelineEdge]


def is_dag_topological(node_ids: List[str], edges: List[PipelineEdge]) -> bool:
    """DAG check using topological sort (Kahn's algorithm)."""
    adjacency = {node_id: [] for node_id in node_ids}
    indegree = {node_id: 0 for node_id in node_ids}

    for edge in edges:
        if edge.source in adjacency and edge.target in adjacency:
            adjacency[edge.source].append(edge.target)
            indegree[edge.target] += 1

    queue = [node_id for node_id, degree in indegree.items() if degree == 0]
    visited = 0

    while queue:
        node_id = queue.pop()
        visited += 1
        for neighbor in adjacency[node_id]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return visited == len(node_ids)


@app.post('/pipelines/parse')
def parse_pipeline(payload: PipelinePayload):
    node_ids = [node.id for node in payload.nodes]
    edge_tuples = [(edge.source, edge.target) for edge in payload.edges]
    num_nodes = len(node_ids)
    num_edges = len(payload.edges)

    is_dag = is_dag_dfs(node_ids, edge_tuples)
  
    cycle = None
    if not is_dag:
        cycle = find_cycle_dfs(node_ids, edge_tuples)

    return {
        'num_nodes': num_nodes,
        'num_edges': num_edges,
        'is_dag': is_dag,
        'cycle': cycle,
    }
