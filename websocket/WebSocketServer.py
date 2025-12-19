import ast
import asyncio
import logging
import time
import functools
import pandas as pd
import websockets
import socket


def write_to_file(message, file):
    with open(file, 'a+') as f:
        f.write("{}\n".format(message))


async def ws_handler(websocket, params, output_file):
    # Log connection
    client_address = websocket.remote_address
    logging.info(f"🔌 Unity connected from {client_address[0]}:{client_address[1]}")
    
    # first sending base parameters to unity (name child etc)
    logging.info(f"📤 Sending {len(params)} initialization message(s) to Unity...")
    for i, param in enumerate(params, 1):
        await websocket.send(str(param))
        logging.info(f"   ✓ Sent message {i}: {list(param.keys())}")
    
    logging.info("✓ All initialization data sent to Unity")
    logging.info("─────────────────────────────────────────────")
    logging.info("📡 Listening for messages from Unity...")
    
    # then handling incoming messages
    try:
        async for message in websocket:
            logging.info(f"📨 Received: {message[:100]}{'...' if len(message) > 100 else ''}")
            write_to_file(message, output_file)
    except websockets.exceptions.ConnectionClosed:
        logging.info("⚠ Unity connection closed")
    except Exception as e:
        logging.error(f"❌ WebSocket error: {e}")
        # message_dict = ast.literal_eval(message)
        # for key, value in message_dict.items():
        #     match key:
        #         case "connectMessage":
        #             print("connected with {}".format(value))
        #         case "_time":
        #             print("connection time is {}".format(value))
        #         case "caregiver_rating":
        #             print("care giver got a rating of {}".format(value))
        #         case default:
        #             print("no know command: {}".format(key))


async def start_ws_server(params=None, output_file="", ip: str = 'localhost',
                          port: int = 8080):
    if params is None:
        params = [{"i": "test", "name": "Charles"}]
    
    logging.info(f"✓ WebSocket server starting on {ip}:{port}")
    
    try:
        # Create the server - websockets library handles SO_REUSEADDR automatically
        server = await websockets.serve(
            functools.partial(ws_handler, params=params, output_file=output_file), 
            ip,
            port,
            family=socket.AF_INET
        )
        
        logging.info(f"✓ Server ready - waiting for Unity connection...")
        
        # Run forever
        await asyncio.Future()
            
    except OSError as e:
        if e.errno == 10048 or "already in use" in str(e).lower():
            logging.error("─────────────────────────────────────────────")
            logging.error(f"❌ Port {port} is already in use!")
            logging.error("⚠ Solution:")
            logging.error("  1. Close any other AddAttachment instances")
            logging.error("  2. Wait 30-60 seconds for the port to be released")
            logging.error("  3. Check Task Manager for 'python.exe' processes")
            logging.error("  4. Or try closing and reopening the application")
            logging.error("")
            logging.error("💡 To find what's using the port, run in PowerShell:")
            logging.error(f"   Get-NetTCPConnection -LocalPort {port}")
            logging.error("─────────────────────────────────────────────")
        else:
            logging.error("─────────────────────────────────────────────")
            logging.error(f"❌ WebSocket Server Error: {e}")
            logging.error("⚠ Common issues:")
            logging.error("  - Is Unity running and trying to connect?")
            logging.error("  - Is the correct network connected?")
            logging.error(f"  - Is port {port} accessible?")
            logging.error("─────────────────────────────────────────────")
        import traceback
        traceback.print_exc()
        input("Press Enter to continue...")
    except Exception as e:
        logging.error("─────────────────────────────────────────────")
        logging.error(f"❌ WebSocket Server Error: {e}")
        logging.error("⚠ Please check the error message above")
        logging.error("─────────────────────────────────────────────")
        import traceback
        traceback.print_exc()
        input("Press Enter to continue...")

if __name__ == '__main__':
    websocket_data = [
        {"player": "Sander"},
        {"contingency": "20"}
    ]
    asyncio.run(start_ws_server(params=websocket_data, output_file="test.csv", ip='192.168.50.188'))
    # loop = asyncio.get_event_loop()
    # task = loop.create_task(startWsServer())
    # try:
    #     loop.run_until_complete(task)
    # except asyncio.CancelledError:
    #     pass
    # while True:
    #     print("a")
    #     time.sleep(2)
