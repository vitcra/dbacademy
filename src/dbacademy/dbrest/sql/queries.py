from dbacademy.dbrest import DBAcademyRestClient
import builtins

from dbacademy.rest.common import ApiContainer


class SqlQueriesClient(ApiContainer):

    def __init__(self, client: DBAcademyRestClient):
        self.client = client
        self.base_uri = f"{self.client.endpoint}/api/2.0/preview/sql/queries"
        self.max_page_size = 250

    def list(self, queries=None, page=1):
        if queries is None:
            queries = builtins.list()

        url = f"{self.base_uri}?page_size={self.max_page_size}&page={page}"
        json_response = self.client.api("GET", url)

        queries.extend(json_response.get("results", builtins.list()))

        if json_response.get("count") == len(queries):
            return queries
        else:
            return self.list(queries=queries, page=page+1)

    def get_by_id(self, query_id):
        return self.client.api("GET", f"{self.base_uri}/{query_id}")

    def delete_by_id(self, query_id):
        return self.client.api("DELETE", f"{self.base_uri}/{query_id}", _expected=(200, 404))

    def undelete_by_id(self, query_id):
        return self.client.api("POST", f"{self.base_uri}/trash/{query_id}")

    def get_by_name(self, query_name, queries=None, page=1):
        if queries is None:
            queries = builtins.list()

        url = f"{self.base_uri}?page_size={self.max_page_size}&page={page}"
        json_response = self.client.api("GET", url)

        queries.extend(json_response.get("results", builtins.list()))

        for query in queries:
            if query_name == query.get("name"):
                return query

        # Not found, continue looking.
        if json_response.get("count") == len(queries):
            return None
        else:
            return self.get_by_name(query_name=query_name, queries=queries, page=page+1)

    def clone(self, query: dict):
        create_def = self.existing_to_create(query)
        create_def["name"] = "Clone - "+create_def["name"]
        return self.create_from_dict(query)

    @staticmethod
    def existing_to_create(query: dict):
        assert type(query) == dict, f"Expected the \"query\" parameter to be of type dict, found {type(query)}"

        for key in list(query.keys()):
            if key not in ["query", "name", "description", "schedule", "options"]:
                del query[key]

        return query

    def create_from_dict(self, params: dict):
        return self.client.api("POST", f"{self.base_uri}", params)

    def create(self, name: str, query: str, description: str = None, schedule: dict = None, options: dict = None, data_source_id: str = None):
        params = dict()
        params["data_source_id"] = data_source_id
        params["query"] = query
        params["name"] = name
        params["description"] = description
        params["schedule"] = schedule
        params["options"] = builtins.dict() if options is None else options
        return self.create_from_dict(params)

    def update_from_dict(self, id_value: str, params: dict):
        assert len(params.keys()) > 0, "Expected at least one parameter."
        return self.client.api("POST", f"{self.base_uri}/{id_value}", params)

    def update(self, id_value: str, name: str = None, query: str = None, description: str = None, schedule: dict = None, options: dict = None, data_source_id: str = None):
        params = dict()

        if name is not None:
            params["name"] = name
        if query is not None:
            params["query"] = query
        if description is not None:
            params["description"] = description
        if schedule is not None:
            params["schedule"] = schedule
        if options is not None:
            params["options"] = builtins.dict() if options is None else options
        if data_source_id is not None:
            params["data_source_id"] = data_source_id
        
        return self.update_from_dict(id_value, params)
