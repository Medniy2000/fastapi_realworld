from strawberry.fastapi import GraphQLRouter

from src.app.graphql.context import get_context
from src.app.graphql.schemas import graphql_schema

graphql_router = GraphQLRouter(graphql_schema, context_getter=get_context)
