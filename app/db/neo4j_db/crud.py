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


def create_with_rel(parent_params: dict, parent_labels: List[str], params: dict, labels: List[str], rel: str):
    params_with_new_keys = {f"ch{key}": value for key, value in params.items()}
    parent_params_with_new_keys = {f"par{key}": value for key, value in parent_params.items()}
    parent_labels_str = f":{":".join(parent_labels)}"
    labels_str = f":{":".join(labels)}"
    parent_properties = "".join([f"p.{prop} = $par{prop} and " for prop in parent_params])[0:-4]
    properties = "".join([f"{prop}:$ch{prop}, " for prop in params])[0:-2]
    query = f"""
            match (p{parent_labels_str})
            where {parent_properties}
            merge (o{labels_str}{{{properties}}}) <-[:{rel}]- (p)
            return o
            """
    return single_query(query=query, params={**params_with_new_keys, **parent_params_with_new_keys})


def delete(params: dict, labels: List[str]):
    labels_str = f":{":".join(labels)}"
    properties = "".join([f"{prop}:${prop}, " for prop in params])[0:-2]
    query = query = f"""
            match (o{labels_str}{{{properties}}})
            delete o
            return o
            """
    return Success("deleted succefully") if single_query(query, params) else Failure("error accoured while deleting")


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


def recreate_with_rel(parent_params, parent_labels, params: dict, labels: List[str]):
    return read_one(params, labels).get("o") \
        or create_with_rel(
            parent_params=parent_params,
            parent_labels=parent_labels,
            params=params,
            labels=labels)



def update(filter_params: dict = {}, new_params: dict = {}, labels: List[str] = []):
    new_params_with_new_keys = {f"new{key}": value for key, value in new_params.items()}
    filter_params_with_new_keys = {f"fil{key}": value for key, value in filter_params.items()}
    labels_str = f":{":".join(labels)}"
    new_properties = "".join([f"set o.{prop} = $new{prop} \n" for prop in new_params])
    filter_properties = "".join([f"o.{prop} = $fil{prop} and " for prop in filter_params])[0:-4]
    query = query = f"""
                    match (o{labels_str})
                    where {filter_properties}
                    {new_properties}
                    return o
                    """
    return single_query(query=query, params={**new_params_with_new_keys, **filter_params_with_new_keys})


def create_two_nodes_with_rel(node_one_params: dict, node_one_labels: List[str], node_two_params: dict, node_two_labels: List[str], rel: str, rel_params: dict):
    node_one_params_with_new_keys = {f"one{key}": value for key, value in node_one_params.items()}
    node_two_params_with_new_keys = {f"two{key}": value for key, value in node_two_params.items()}
    rel_params_with_new_keys = {f"rel{key}": value for key, value in rel_params.items()}
    node_one_labels_str = f":{":".join(node_one_labels)}"
    node_two_labels_str = f":{":".join(node_two_labels)}"
    node_one_properties = "".join([f"{prop}:$one{prop}, " for prop in node_one_params])[0:-2]
    node_two_properties = "".join([f"{prop}:$two{prop}, " for prop in node_two_params])[0:-2]
    rel_properties = "".join([f"{prop}:$rel{prop}, " for prop in rel_params])[0:-2]
    query = f"""
                create (n1{node_one_labels_str}{{{node_one_properties}}})
                create (n2{node_two_labels_str}{{{node_two_properties}}})
                merge (n1) -[rel:{rel}{{{rel_properties}}}]- (n2)
                return rel
                """
    return single_query(query=query, params={**node_one_params_with_new_keys, **node_two_params_with_new_keys, **rel_params_with_new_keys})