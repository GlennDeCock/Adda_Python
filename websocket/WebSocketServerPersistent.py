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


async def ws_handler(websocket, params, output_file):
    """Improved websocket handler that maintains persistent connections"""
    client_address = websocket.remote_address
    print(f"🔗 New client connected from {client_address}")
    
    try:
        # Send base parameters to Unity (player config etc)
        for param in params:
            param_str = json.dumps(param) if isinstance(param, dict) else str(param)
            await websocket.send(param_str)
            print(f"📤 Sent to {client_address}: {param_str}")
        
        # Keep connection alive and handle incoming messages
        print(f"👂 Listening for messages from {client_address}...")
        
        while True:
            try:
                # Wait for messages with a reasonable timeout
                message = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                
                # Log the received message
                timestamp = int(time.time())
                log_entry = f"time: {timestamp}, {message}"
                print(f"📨 Received from {client_address}: {message}")
                write_to_file(log_entry, output_file)
                
                # Optional: Send acknowledgment back to Unity
                # await websocket.send(json.dumps({"status": "received", "timestamp": timestamp}))
                
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                try:
                    await websocket.ping()
                    print(f"🏓 Ping sent to {client_address}")
                except:
                    print(f"❌ Lost connection to {client_address}")
                    break
                    
            except websockets.exceptions.ConnectionClosed:
                print(f"🔌 Client {client_address} disconnected normally")
                break
                
            except Exception as e:
                print(f"⚠️ Error handling message from {client_address}: {e}")
                # Don't break the loop for message handling errors
                continue
                
    except websockets.exceptions.ConnectionClosed:
        print(f"🔌 Client {client_address} connection closed")
    except Exception as e:
        print(f"❌ Connection error with {client_address}: {e}")
    finally:
        print(f"🧹 Cleaned up connection for {client_address}")


async def start_ws_server(params=None, output_file="", ip: str = 'localhost',
                          port: int = 8080):
    """Start websocket server with improved connection handling"""
    if params is None:
        params = [{"i": "test", "name": "Charles"}]
    
    print("🚀 Starting websocket server with params:", params)
    print(f"📡 Server will listen on {ip}:{port}")
    print(f"💾 Data will be saved to: {output_file}")
    
    try:
        # Create the websocket server
        server = await websockets.serve(
            functools.partial(ws_handler, params=params, output_file=output_file), 
            ip, 
            port,
            ping_interval=20,  # Send ping every 20 seconds
            ping_timeout=10,   # Wait 10 seconds for pong
            close_timeout=10   # Wait 10 seconds for close
        )
        
        print("✅ Websocket server started successfully!")
        print("🎮 Unity can now connect and stay connected!")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Keep the server running
        await server.wait_closed()
        
    except Exception as e:
        logging.error(f"Server error: {e}")
        logging.error("Is the computer connected to the correct network?")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    websocket_data = [
        {"player": "Sander"},
        {"contingency": "20"}
    ]
    asyncio.run(start_ws_server(params=websocket_data, output_file="test.csv", ip='localhost'))
