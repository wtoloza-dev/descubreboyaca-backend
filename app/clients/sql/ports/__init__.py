"""SQL client ports (Hexagonal Architecture).

This package contains Port definitions that define the contracts
for SQL database clients. These are PORTS in Hexagonal Architecture (Ports and Adapters pattern).
"""

from app.clients.sql.ports.asynchronous import AsyncSQLClientPort
from app.clients.sql.ports.synchronous import SQLClientPort


__all__ = ["SQLClientPort", "AsyncSQLClientPort"]
