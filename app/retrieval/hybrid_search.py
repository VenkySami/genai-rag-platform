from app.retrieval.graph_search import search_graph
from app.retrieval.vector_search import search_vector


def hybrid_retrieve(vector_store, query):

    vector_results = search_vector(vector_store, query)

    graph_results = search_graph(query)

    return vector_results, graph_results
