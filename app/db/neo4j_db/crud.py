from typing import List
from returns.result import Result, Success, Failure
from app.db.neo4j_db.database import get_driver


def single_query(query: str, params: dict={}):
    with get_driver().session()as session:
        return session.run(query=query, parameters=params).single()


def data_query(query: str, params: dict={}):
    with get_driver().session()as session:
        return session.run(query=query, parameters=params).data()


def create(params: dict, labels: List[str]):
    labels_str = f":{":".join(labels)}"
    properties = "".join([f"{prop}:${prop}, " for prop in params])[0:-2]
    query = f"create (o{labels_str}{{{properties}}}) return o"
    return single_query(query, params)



def read_all(params: dict = {} ,labels: List[str] = []):
    labels_str = f":{":".join(labels)}"
    properties = "".join([f"{prop}:${prop}, " for prop in params])[0:-2]
    query = query = f"""
                match (o{labels_str}{{{properties}}})
                return o
                """
    return data_query(query=query, params=params)


def read_one(params: dict = {} ,labels: List[str] = []):
    labels_str = f":{":".join(labels)}"
    properties = "".join([f"{prop}:${prop}, " for prop in params])[0:-2]
    query = query = f"""
                match (o{labels_str}{{{properties}}})
                return o
                """
    return single_query(query=query, params=params)


def merge(node_one_params: dict, node_one_labels: List[str], node_two_params: dict, node_two_labels: List[str], rel: str, rel_params: dict):
    node_one_params_with_new_keys = {f"one{key}": value for key, value in node_one_params.items()}
    node_two_params_with_new_keys = {f"two{key}": value for key, value in node_two_params.items()}
    rel_params_with_new_keys = {f"rel{key}": value for key, value in rel_params.items()}
    node_one_labels_str = f":{":".join(node_one_labels)}"
    node_two_labels_str = f":{":".join(node_two_labels)}"
    node_one_properties = "".join([f"{prop}:$one{prop}, " for prop in node_one_params])[0:-2]
    node_two_properties = "".join([f"{prop}:$two{prop}, " for prop in node_two_params])[0:-2]
    rel_properties = "".join([f"{prop}:$rel{prop}, " for prop in rel_params])[0:-2]
    query = f"""
            match (n1{node_one_labels_str}{{{node_one_properties}}})
            match (n2{node_two_labels_str}{{{node_two_properties}}})
            merge (n1) -[rel:{rel}{{{rel_properties}}}]- (n2)
            return rel
            """
    return single_query(query=query, params={**node_one_params_with_new_keys, **node_two_params_with_new_keys, **rel_params_with_new_keys})




def recreate(params: dict, labels: List[str]):
    return read_one(params, labels) \
        or create(params, labels)

