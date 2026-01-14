import websocket
import threading
import time
import sys

# Enable verbose usage
websocket.enableTrace(True)

def test_url(url):
    print(f"--- Testing URL: {url} ---")
    
    def on_open(ws):
        print(f"[{url}] OPENED")
        def run(*args):
             time.sleep(2)
             ws.close()
        threading.Thread(target=run).start()

    def on_error(ws, error):
        print(f"[{url}] ERROR: {error}")

    def on_close(ws, close_status_code, close_msg):
        print(f"[{url}] CLOSED: {close_status_code} - {close_msg}")

    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_error=on_error,
        on_close=on_close
    )
    
    ws.run_forever()
    print(f"--- Finished {url} ---\n")

if __name__ == "__main__":
    urls = [
        "wss://bullapitest.1bullex.com/ws/kline",
        "wss://bullapitest.1bullex.com/ws",
        "wss://echo.websocket.org", # Baseline test
    ]
    
    for u in urls:
        test_url(u)
