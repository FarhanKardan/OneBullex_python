import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from onebullex import OneBullExWebSocket, constants
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def main():
    print("Testing OneBullEx WebSocket Client (Public)...")
    
    # Use Test Environment
    ws = OneBullExWebSocket(url=constants.TEST_WS_URL)
    
    def on_kline(data):
        print(f"[WS] Received Kline Data: {data}")
        
    try:
        print("Starting WebSocket...")
        ws.start()
        
        if not ws.wait_for_connection(timeout=10):
            print("Failed to connect to WebSocket.")
            return

        print("WebSocket connected!")
        
        # Use a likely valid symbol, e.g., ADA_USDT or from REST check. 
        # Hardcoding ADA_USDT based on previous REST output.
        symbol = "ADA_USDT"
        print(f"Subscribing to {symbol} (Future Kline 1m)...")
        ws.subscribe_kline(symbol, "1m", on_kline, is_spot=False)
        
        print("Waiting for data (30s)...")
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        ws.stop()
        print("Done.")

if __name__ == "__main__":
    main()
