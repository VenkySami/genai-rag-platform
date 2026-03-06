from app.graph_db.neo4j_client import driver


def search_graph(query):
    """Return graph results from Neo4j. If Neo4j is unavailable, return [] so chat still works with vector-only."""
    cypher = """
    MATCH (a)-[r]->(b)
    WHERE a.name CONTAINS $query
    RETURN a,r,b
    """
    try:
        with driver.session() as session:
            result = session.run(cypher, {"query": query})
            return [record.data() for record in result]
    except Exception:
        return []
