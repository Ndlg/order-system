from fastapi import APIRouter

from app.api.routes import auth, health, resources


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

for route_prefix, resource_name, tag in resources.RESOURCE_ROUTES:
    api_router.include_router(
        resources.build_resource_router(resource_name, tag),
        prefix=route_prefix,
        tags=[tag],
    )
