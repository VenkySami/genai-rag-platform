from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

def create_relation(entity1, relation, entity2):

    query = """
    MERGE (a:Concept {name:$e1})
    MERGE (b:Concept {name:$e2})
    MERGE (a)-[:RELATION {type:$rel}]->(b)
    """

    with driver.session() as session:
        session.run(query, e1=entity1, e2=entity2, rel=relation)
