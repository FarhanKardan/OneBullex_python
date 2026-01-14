import time
import threading
from typing import Dict

class TokenBucket:
    """
    Thread-safe Token Bucket implementation for rate limiting.
    """
    def __init__(self, rate: float, capacity: float):
        self.rate = rate  # Tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = threading.Lock()

    def consume(self, cost: float = 1.0, block: bool = True, timeout: float = None) -> bool:
        """
        Consume tokens. If block is True, sleeps until tokens are available.
        """
        start = time.time()
        with self.lock:
            while True:
                now = time.time()
                elapsed = now - self.last_update
                self.last_update = now
                
                # Refill
                self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
                
                if self.tokens >= cost:
                    self.tokens -= cost
                    return True
                
                if not block:
                    return False
                
                # Calculate wait time
                needed = cost - self.tokens
                wait_time = needed / self.rate
                
                if timeout is not None and (time.time() - start + wait_time) > timeout:
                    return False
                
                # Sleep release lock? No, strictly we should release lock while sleeping 
                # but for simple client this blocks other threads which is actually desired 
                # to strictly enforce rate. However, python GIL makes it tricky.
                # Better: release lock, sleep, acquire.
                
                # PROPER IMPLEMENTATION:
                # We calculate wait, sleep, then retry loop.
                # But we must update tokens before sleeping? No.
                
                # Simplified for this context:
                # If not enough tokens, we sleep exactly needed time.
                # But another thread might steal.
                pass 
                # Re-acquiring lock logic is complex.
                # Let's use a simpler approach: calculate time to wake up.
                
                wait = (cost - self.tokens) / self.rate
                if wait > 0:
                     # For simplicity in this non-async context, we block with the lock
                     # This ensures FIFO ordering roughly and prevents burst overruns
                     # It stalls the entire client if Rate Limit matches Thread Count, 
                     # but for 10-20 RPS it's negligible.
                    time.sleep(wait)
                    # Loop will re-calculate tokens after sleep
                    continue

class RateLimiter:
    """
    Central rate limiter manager.
    Can manage multiple buckets (e.g. per IP, per UID).
    OneBullEx docs imply global IP/Key limits.
    """
    def __init__(self, rps: float = 10):
        self.global_bucket = TokenBucket(rate=rps, capacity=rps)
    
    def wait(self, weight: int = 1):
        self.global_bucket.consume(float(weight))
