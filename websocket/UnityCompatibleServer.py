import ast
import asyncio
import logging
import time
import functools
import pandas as pd
import websockets
import json


def write_to_file(message, file):
    with open(file, 'a+') as f:
        f.write("{}\n".format(message))


async def unity_compatible_handler(websocket, params, output_file):
    """Unity-compatible websocket handler without aggressive ping/pong"""
    client_address = websocket.remote_address
    print(f"🔗 Unity client connected from {client_address}")
    
    try:
        # Send base parameters to Unity
        for param in params:
            param_str = json.dumps(param) if isinstance(param, dict) else str(param)
            await websocket.send(param_str)
            print(f"📤 Sent config to Unity: {param_str[:100]}...")
        
        print(f"👂 Listening for Unity messages...")
        
        # Simple message loop without timeouts that might confuse Unity
        async for message in websocket:
            try:
                # Log the received message
                timestamp = int(time.time())
                log_entry = f"time: {timestamp}, {message}"
                print(f"📨 Unity says: {message}")
                write_to_file(log_entry, output_file)
                
                # Optional: Send simple acknowledgment
                # await websocket.send(json.dumps({"received": True}))
                
            except Exception as e:
                print(f"⚠️ Error processing Unity message: {e}")
                continue
                
    except websockets.exceptions.ConnectionClosed:
        print(f"🔌 Unity disconnected normally")
    except Exception as e:
        print(f"❌ Unity connection error: {e}")
    finally:
        print(f"🧹 Unity connection cleaned up")


async def start_unity_server(params=None, output_file="", ip: str = 'localhost',
                          port: int = 8080):
    """Start Unity-compatible websocket server"""
    if params is None:
        params = [{"i": "test", "name": "Charles"}]
    
    print("🎮 Starting Unity-compatible websocket server...")
    print(f"📡 Listening on {ip}:{port}")
    print(f"💾 Logging to: {output_file}")
    
    try:
        # Create server with Unity-friendly settings
        async with websockets.serve(
            functools.partial(unity_compatible_handler, params=params, output_file=output_file), 
            ip, 
            port,
            ping_interval=None,  # Disable ping to avoid Unity compatibility issues
            ping_timeout=None,   # Disable ping timeout
            close_timeout=10,    # Keep close timeout reasonable
            max_size=1000000     # Allow larger messages
        ) as server:
            print("✅ Unity server ready!")
            print("🔗 Unity can now connect and stay connected!")
            await asyncio.Future()  # run forever
        
    except Exception as e:
        logging.error(f"Unity server error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    websocket_data = [
        {"type": "player", "playerValues": {"name": "TestPlayer", "contingency": 20}}
    ]
    asyncio.run(start_unity_server(params=websocket_data, output_file="unity_test.csv", ip='localhost'))
