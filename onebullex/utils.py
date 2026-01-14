import logging
import time
from typing import Optional

# Safe logger that can be configured centrally
logger = logging.getLogger("onebullex")
logger.addHandler(logging.NullHandler())

class TimeSync:
    """
    Handles server time synchronization to prevent 'Timestamp expired' errors.
    Calculates clock drift between local machine and server.
    """
    def __init__(self):
        self._offset_ms: int = 0
        self._last_sync: float = 0
        self._sync_interval: float = 300 # 5 minutes

    def update(self, server_time_ms: int):
        """Update the offset based on server time from a response header or payload."""
        local_time_ms = int(time.time() * 1000)
        # Server = Local + Offset
        # Offset = Server - Local
        self._offset_ms = server_time_ms - local_time_ms
        self._last_sync = time.time()
        logger.debug(f"Time synced. Drift: {self._offset_ms}ms")

    def get_server_time_ms(self) -> int:
        """Get estimated server time in milliseconds."""
        return int(time.time() * 1000) + self._offset_ms

    def get_timestamp_str(self) -> str:
        return str(self.get_server_time_ms())
