import sys
import os
import time
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from onebullex import OneBullExWebSocket, TEST_CONFIG

# Configure Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("verify_ws")

def main():
    print("Initializing OneBullEx WebSocket (v2)...")
    
    # Use Test Config URL
    ws_url = TEST_CONFIG.ws_url
    logger.info(f"Connecting to {ws_url}...")
    
    ws = OneBullExWebSocket(url=ws_url)
    
    def on_kline(data):
        logger.info(f"Received Kline Data: {data}")

    try:
        ws.start()
        
        logger.info("Waiting for connection (10s timeout)...")
        if ws.wait_for_connection(timeout=10):
            logger.info("Connected!")
            
            # Subscribe
            symbol = "ADA_USDT" # Known valid component from REST check
            logger.info(f"Subscribing to {symbol} kline...")
            ws.subscribe_kline(symbol, "1m", on_kline, is_spot=True)
            
            logger.info("Listening for 20 seconds...")
            time.sleep(20)
        else:
            logger.error("Failed to connect to WebSocket.")
            
    except KeyboardInterrupt:
        logger.info("Interrupted.")
    finally:
        ws.stop()
        logger.info("Stopped.")

if __name__ == "__main__":
    main()
