"""DAG detection utilities using DFS cycle detection."""

from typing import List, Tuple


def is_dag_dfs(nodes: List[str], edges: List[Tuple[str, str]]) -> bool:
    """
    Check if a directed graph is a DAG using DFS cycle detection.
    
    A graph is a DAG (Directed Acyclic Graph) if and only if it contains no cycles.
    Uses DFS with color-based state tracking:
    - White (0): Unvisited
    - Gray (1): Currently in recursion stack
    - Black (2): Completely processed
    
    Args:
        nodes: List of node identifiers
        edges: List of (source, target) tuples representing directed edges
        
    Returns:
        True if the graph is a DAG, False if a cycle is detected
    """
    adjacency = {node: [] for node in nodes}
    for source, target in edges:
        if source in adjacency and target in adjacency:
            adjacency[source].append(target)
    
    color = {node: 0 for node in nodes}
    
    def dfs(node: str) -> bool:
        """
        DFS helper function.
        
        Returns:
            False if a cycle is detected, True otherwise
        """
        color[node] = 1  
        
        for neighbor in adjacency[node]:
            if color[neighbor] == 1:
                return False
            elif color[neighbor] == 0:
                if not dfs(neighbor):
                    return False
        
        color[node] = 2  
        return True
    
    for node in nodes:
        if color[node] == 0:
            if not dfs(node):
                return False
    
    return True


def find_cycle_dfs(nodes: List[str], edges: List[Tuple[str, str]]) -> List[str] | None:
    """
    Find a cycle in a directed graph using DFS, if one exists.
    
    Args:
        nodes: List of node identifiers
        edges: List of (source, target) tuples representing directed edges
        
    Returns:
        List of nodes forming a cycle, or None if the graph is a DAG
    """
    adjacency = {node: [] for node in nodes}
    for source, target in edges:
        if source in adjacency and target in adjacency:
            adjacency[source].append(target)
    
    color = {node: 0 for node in nodes}
    parent = {node: None for node in nodes}
    
    def dfs(node: str, path: List[str]) -> List[str] | None:
        """
        DFS helper to detect and return cycle.
        
        Returns:
            Cycle path if found, None otherwise
        """
        color[node] = 1  
        path.append(node)
        
        for neighbor in adjacency[node]:
            if color[neighbor] == 1:
                cycle_start_idx = path.index(neighbor)
                return path[cycle_start_idx:] + [neighbor]
            elif color[neighbor] == 0:
                result = dfs(neighbor, path.copy())
                if result:
                    return result
        
        color[node] = 2  
        return None
    
    for node in nodes:
        if color[node] == 0:
            cycle = dfs(node, [])
            if cycle:
                return cycle
    
    return None
