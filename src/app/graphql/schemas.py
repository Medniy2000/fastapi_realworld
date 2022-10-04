import strawberry
from strawberry.schema.config import StrawberryConfig
from src.app.graphql.queries.query import Query

graphql_schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
