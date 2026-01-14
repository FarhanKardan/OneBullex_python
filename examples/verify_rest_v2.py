import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from onebullex import OneBullExClient, TEST_CONFIG, OrderSide, OrderType

# Configure Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

def main():
    print("Initializing OneBullEx Client (v2 Architecture)...")
    
    # Init Client
    client = OneBullExClient(config=TEST_CONFIG)
    
    try:
        # 1. Market Data
        print("\n[1] Fetching Market Summary...")
        summary = client.market.summary()
        print(f"Success. Fetched {len(summary)} symbols.")
        
        # 2. Tickers
        print("\n[2] Fetching Tickers...")
        tickers = client.market.ticker()
        first_pair = list(tickers.keys())[0] if tickers else "None"
        print(f"First Pair: {first_pair} -> {tickers.get(first_pair)}")
        
        # 3. Klines
        if first_pair != "None":
            print(f"\n[3] Fetching Klines for {first_pair}...")
            klines = client.market.klines(first_pair, "1m")
            if klines and 'list' in klines:
                print(f"Fetched {len(klines['list'])} candles.")
            else:
                 print(f"Raw Kline Response: {klines}")
                 
            # 4. Orderbook
            print(f"\n[4] Fetching Orderbook for {first_pair}...")
            depth = client.market.orderbook(first_pair)
            if depth and 'bids' in depth:
                print(f"Success. Bids: {len(depth['bids'])}, Asks: {len(depth['asks'])}")
            else:
                print(f"Failed Orderbook: {depth}")

            # 5. Trades
            print(f"\n[5] Fetching Trades for {first_pair}...")
            trades = client.market.trades(first_pair)
            print(f"Success. Fetched {len(trades.get('list', []))} trades.")

        # 6. Assets
        print("\n[6] Fetching supported assets...")
        assets = client.market.assets()
        print(f"Success. Fetched {len(assets)} assets.")

        # 7. Contract Info
        print("\n[7] Fetching Contract List...")
        contracts = client.market.contract_list()
        print(f"Success. Fetched {len(contracts.get('list', []))} contracts.")
        
        print("\n[8] Fetching Contract Specs...")
        specs = client.market.contract_specs()
        print(f"Success. Fetched {len(specs.get('list', []))} specs.")


    except Exception as e:
        print(f"Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
