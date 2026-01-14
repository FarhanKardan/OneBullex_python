import threading
import time
import websocket
import logging
from typing import Dict, Callable, Any
from . import constants
from . import messages_pb2 as pb

class OneBullExWebSocket:
    def __init__(self, url: str = constants.PROD_WS_URL):
        self.url = url
        self.ws = None
        self.wst = None
        self.is_running = False
        self.callbacks: Dict[int, Callable] = {} # Action -> Callback
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.is_running = True
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()

    def stop(self):
        self.is_running = False
        if self.ws:
            self.ws.close()
        if self.wst:
            self.wst.join()

    def wait_for_connection(self, timeout: int = 10):
        start = time.time()
        while time.time() - start < timeout:
            if self.ws and self.ws.sock and self.ws.sock.connected:
                return True
            time.sleep(0.1)
        return False

    def _on_open(self, ws):
        self.logger.info("WebSocket Connected")

    def _on_error(self, ws, error):
        self.logger.error(f"WebSocket Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        self.logger.info("WebSocket Closed")

    def _on_message(self, ws, message):
        try:
            # Parse BaseMessage
            base_msg = pb.BaseMessage()
            base_msg.ParseFromString(message)
            
            action = base_msg.action
            data = base_msg.data
            
            # Dispatch to callback
            if action in self.callbacks:
                self.callbacks[action](data)
            else:
                self.logger.debug(f"Received unhandled action: {action}")
                
        except Exception as e:
            self.logger.error(f"Error parsing message: {e}")

    def _send_pb(self, action: int, pb_obj):
        if not self.ws or not self.ws.sock or not self.ws.sock.connected:
            self.logger.error("WebSocket is not connected")
            return

        base_msg = pb.BaseMessage()
        base_msg.action = action
        base_msg.time = int(time.time() * 1000)
        base_msg.data = pb_obj.SerializeToString()
        
        binary_data = base_msg.SerializeToString()
        self.ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

    # --- Subscriptions ---

    def subscribe_kline(self, symbol: str, period: str, callback: Callable[[Any], None], is_spot: bool = False):
        """
        Subscribe to Kline.
        is_spot=True -> Spot Kline (Assumed Action 10002, Push 20002)
        is_spot=False -> Future Kline (Assumed Action 10003, Push 20003)
        """
        sub_info = pb.SendSubscribeInfo()
        sub_info.symbol = symbol
        sub_info.period = period
        sub_info.platform = ""
        
        # Use inferred actions
        sub_action = 10002 if is_spot else 10003
        push_action = 20002 if is_spot else 20003
        
        # Register callback for the response/push action
        # Note: Valid parsing requires knowing the structure (RecKlineData)
        def wrapper(data):
            parsed = pb.RecKlineData()
            parsed.ParseFromString(data)
            callback(parsed)
            
        self.callbacks[push_action] = wrapper
        
        self._send_pb(sub_action, sub_info)

    def subscribe_depth(self, symbol: str, callback: Callable[[Any], None]):
        """
        Subscribe to Order Book Depth (Futures).
        Assumed Action 10007, Push 20007
        """
        sub_info = pb.SendSubscribeDepth()
        sub_info.symbol = symbol
        sub_info.platform = ""
        
        push_action = 20007
        
        def wrapper(data):
            parsed = pb.RecDepthInfo()
            parsed.ParseFromString(data)
            callback(parsed)
            
        self.callbacks[push_action] = wrapper
        
        self._send_pb(10007, sub_info)

    def subscribe_trades(self, callback: Callable[[Any], None]):
        """
        Subscribe to Recent Trades (Futures).
        Assumed Action 10004 (Guess based on pattern), Push 20004 (Guess)
        WARNING: Action IDs are speculative.
        """
        sub_info = pb.SendSubscribeTicker()
        sub_info.platform = ""
        
        # Speculative IDs
        sub_action = 10004 
        push_action = 20004
        
        def wrapper(data):
            parsed = pb.RecKlineData() # "Same as kline data push format"
            parsed.ParseFromString(data)
            callback(parsed)
            
        self.callbacks[push_action] = wrapper
        
        self._send_pb(sub_action, sub_info)
