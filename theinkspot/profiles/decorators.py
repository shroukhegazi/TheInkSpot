from django.db import connection, reset_queries


def database_debug(func):
    """Use this decorator to see the queries evaluated by your function"""

    def inner_func(*args, **kwargs):
        reset_queries()
        results = func()
        query_info = connection.queries
        print("function_name: {}".format(func.__name__))
        print("query_count: {}".format(len(query_info)))
        queries = ["{}\n".format(query["sql"]) for query in query_info]
        print("queries: \n{}".format("".join(queries)))
        return results

    return inner_func
