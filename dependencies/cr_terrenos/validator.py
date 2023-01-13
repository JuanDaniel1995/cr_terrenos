from lambda_handlers.errors import BadRequestError

class Validator:
    @classmethod
    def query_parameters_present(self, event, required_params=[]):
        query_parameters = (
            event.get("queryStringParameters")
            if ("queryStringParameters") in event
            else None
        )

        if not (query_parameters):
            raise BadRequestError("This request requires additional parameters.")

        for param in required_params:
            if not query_parameters.get(param, None):
                raise BadRequestError(f"Missing required parameter {param}")
        return query_parameters

    @classmethod
    def path_parameters_present(self, event, required_params=[]):
        path_parameters = event["pathParameters"] if "pathParameters" in event else None

        if not path_parameters:
            raise BadRequestError("This request requires additional parameters.")
        
        for param in required_params:
            if not path_parameters.get(param, None):
                raise BadRequestError(f"Missing required parameter {param}")
        return path_parameters

    @classmethod
    def body_parameters_present(self, body, required_params=[]):
        if not body:
            raise BadRequestError("This request requires additional parameters.")
        
        for param in required_params:
            if body.get(param, None) == None:
                raise BadRequestError(f"Missing required parameter {param}")
        return body