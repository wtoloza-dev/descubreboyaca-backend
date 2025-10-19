"""SQL client ports (Hexagonal Architecture).

This package contains Protocol definitions that define the contracts
for SQL database clients. These are PORTS in Hexagonal Architecture (Ports and Adapters pattern).
"""

from app.clients.sql.ports.async_sql import AsyncSQLClientProtocol
from app.clients.sql.ports.sql import SQLClientProtocol


__all__ = ["SQLClientProtocol", "AsyncSQLClientProtocol"]
