# Install Azure Cosmos DB SDK if not already
pip install azure-cosmos

import logging
from typing import Optional, TypedDict, Union

from azure.cosmos import CosmosClient

from .abstract_cache_base import AbstractCache
from .disk_cache import DiskCache


class CosmosDBConfig(TypedDict, total=False):
    connection_string: str
    database_id: str
    container_id: str
    cache_seed: Optional[Union[str, int]]
    client: Optional[CosmosClient]


class CacheFactory:
    @staticmethod
    def cache_factory(
        seed: Union[str, int],
        redis_url: Optional[str] = None,
        cache_path_root: str = ".cache",
        cosmosdb_config: Optional[CosmosDBConfig] = None,
    ) -> AbstractCache:
        """
        Factory function for creating cache instances.

        This function decides whether to create a RedisCache, DiskCache, or CosmosDBCache instance
        based on the provided parameters. If RedisCache is available and a redis_url is provided,
        a RedisCache instance is created. If connection_string, database_id, and container_id
        are provided, a CosmosDBCache is created. Otherwise, a DiskCache instance is used.

        Args:
            seed (Union[str, int]): Used as a seed or namespace for the cache.
            redis_url (Optional[str]): URL for the Redis server.
            cache_path_root (str): Root path for the disk cache.
            cosmosdb_config (Optional[Dict[str, str]]): Dictionary containing 'connection_string',
                                                       'database_id', and 'container_id' for Cosmos DB cache.

        Returns:
            An instance of RedisCache, DiskCache, or CosmosDBCache.

        Examples:

        Creating a Redis cache

        ```python
        redis_cache = cache_factory("myseed", "redis://localhost:6379/0")
        ```
        Creating a Disk cache

        ```python
        disk_cache = cache_factory("myseed", None)
        ```

        Creating a Cosmos DB cache:
        ```python
        cosmos_cache = cache_factory("myseed", cosmosdb_config={
                "connection_string": "your_connection_string",
                "database_id": "your_database_id",
                "container_id": "your_container_id"}
            )
        ```

        """
        if redis_url:
            try:
                from .redis_cache import RedisCache

                return RedisCache(seed, redis_url)
            except ImportError:
                logging.warning(
                    "RedisCache is not available. Checking other cache options. The last fallback is DiskCache."
                )

        if cosmosdb_config and all(
            key in cosmosdb_config for key in ["connection_string", "database_id", "container_id"]
        ):
            try:
                from .cosmos_db_cache import CosmosDBCache

                return CosmosDBCache(seed, **cosmosdb_config)
            except ImportError:
                logging.warning("CosmosDBCache is not available. Fallback to DiskCache.")

        # Default to DiskCache if neither Redis nor Cosmos DB configurations are provided
        return DiskCache(f"./{cache_path_root}/{seed}")
