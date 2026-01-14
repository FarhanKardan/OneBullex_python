import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from onebullex import RestClient, constants

def main():
    print("Testing OneBullEx REST Client (Public API)...")
    
    # Use Test Environment
    client = RestClient(base_url=constants.TEST_REST_URL)
    
    try:
        # 1. Spot Summary
        print("\n1. Fetching Spot Market Summary...")
        summary = client.get_spot_summary()
        print(f"Success! Received {len(summary)} symbols.")
        # Print first one as sample
        first_sym = list(summary.keys())[0]
        print(f"Sample ({first_sym}): {summary[first_sym]}")
        
        # 2. Supported Assets
        print("\n2. Fetching Supported Assets...")
        assets = client.get_supported_assets()
        print(f"Success! Received {len(assets)} assets.")
        
        # 3. Klines
        first_sym = list(summary.keys())[0]
        print(f"\n3. Fetching Klines for {first_sym} (1m)...")
        klines = client.get_kline_data(first_sym, "1m")
        
        if klines and 'list' in klines:
            print(f"Success! Received {len(klines['list'])} klines.")
        elif klines:
             print(f"Success? Data: {klines}")
        else:
            print(f"Failed: Data is None. Response might be empty for this symbol.")

    except Exception as e:
        print(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
