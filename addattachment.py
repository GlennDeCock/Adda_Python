"""
entry file for the addattachment project
In this file, we'll:
1. have a GUI for entering player name?
2. setup of directory structure
3. three different processes for capturing data:
    - open the websocket towards unity
    - start capturing the EEG datastream + insert markers based on LSL markers
    - capture OSC messages of Emotibit Oscilloscope

We'll try to make an executable of this project using PyInstaller
"""
import asyncio
import logging
import os
import sys
import threading
from datetime import datetime
from tkinter import Tk, simpledialog

# from brainflow import BoardIds

# from eeg.brainflow_get_data import EEG
# from lsl.LSL_ReceiveData import LSLReceptor
from Player.PlayerSession import PlayerSession
from utils.GUI_improved import ImprovedGUI
from utils.utils import *
from websocket.WebSocketServer import start_ws_server
import atexit

# eeg = False
# gsr = False
ws = True
# lsl = False

# def stop_all(websocket, eeg, gsr):
#     eeg.stop_eeg()


if __name__ == '__main__':
    # Configure logging first
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    logging.info("═══════════════════════════════════════════")
    logging.info("  AddAttachment - Starting Application")
    logging.info("═══════════════════════════════════════════")
    
    gui = ImprovedGUI()
    gui.mainloop()
    
    # Check if form was completed
    if not gui.form_completed:
        logging.warning("Application closed without completing form")
        sys.exit(0)
    
    logging.info("─────────────────────────────────────────────")
    logging.info("📋 Processing participant information...")
    
    # load the config file - use the script's directory, not current working directory
    # For PyInstaller executables, use sys.executable location instead of __file__
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        script_dir = Path(sys.executable).parent
    else:
        # Running as script
        script_dir = Path(__file__).parent
    
    config = load_config(script_dir / "conf.yaml")
    logging.info("✓ Configuration loaded")
    
    # Get results including starting support
    gui_results = gui.get_results()
    support = gui_results.get("starting_support", "mama")  # Get from GUI results
    language = gui_results.get("language", "dutch")  # Get language choice
    
    # make a player object to keep track of variables
    player = PlayerSession(gui_results, datetime.now().strftime("%Y_%m_%d__%H_%M"))
    logging.info(f"✓ Player session created: {player.name} (ID: {player.id})")
    
    # Use local data directory instead of system directory
    # root_data_path = create_folder_structure(player.playtime, config)  # Comment out this line
    
    # Create local data directory structure relative to script location
    logging.info("📁 Creating data directories...")
    root_data_path = script_dir / "data" / player.playtime
    root_data_path.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for different data types
    (root_data_path / "websocket").mkdir(exist_ok=True)
    (root_data_path / "eeg").mkdir(exist_ok=True)
    (root_data_path / "gsr").mkdir(exist_ok=True)
    
    logging.info(f"✓ Data directory: {root_data_path}")
    
    # create a config file keeping track of all settings for that child
    player.create_player_conf(location=root_data_path, file_name="player_config.json")
    logging.info("✓ Player configuration saved")
    
    # Log the selected support figure (no popup needed - already selected in GUI)
    logging.info("─────────────────────────────────────────────")
    if support == "mama":
        logging.info("✓ Starting figure: Mama (brown hair, green shirt)")
    else:
        logging.info("✓ Starting figure: Alternative (blonde hair, white shirt)")
    
    logging.info(f"✓ Language: {language.capitalize()}")

    # Build initial messages to send to Unity on connect
    logging.info("─────────────────────────────────────────────")
    logging.info("📦 Preparing WebSocket data for Unity...")
    websocket_data = [{"type": "player",
                       "playerValues": {
                           "name": player.name,
                           "height": player.height,
                           "gender": player.gender,
                           "contingency": player.contingency,
                           "trial_block": player.trial_block,
                           "trial_number": player.trial_number,
                           "support_frequency": player.support_frequency,  # Simplified: direct frequency
                           "language": language  # Language selection
                       }},
                      # New: starting support message for Unity
                      {"websocketMessage": "startingSupport", "support": support}]
    
    logging.info(f"✓ Player data prepared:")
    logging.info(f"  - Name: {player.name}")
    logging.info(f"  - Gender: {player.gender}, Age: {player.age}")
    logging.info(f"  - Contingency: {player.contingency}%")
    logging.info(f"  - Trial Block: {player.trial_block}")
    logging.info(f"  - Starting Trial: {player.trial_number}")
    logging.info(f"  - Support Frequency: {player.support_frequency}")
    logging.info(f"  - Starting Figure: {support}")
    logging.info(f"  - Language: {language}")
    
    logging.info("─────────────────────────────────────────────")
    logging.info("🌐 Starting WebSocket server...")
    logging.info(f"   Listening on {config['DATA_CAPTURE']['WS']['IP']}:{config['DATA_CAPTURE']['WS']['PORT']}")
    logging.info("   Waiting for Unity to connect...")

    # Run WebSocket server in a separate thread so GUI stays responsive
    def run_websocket_server():
        """Run the websocket server in its own event loop"""
        try:
            asyncio.run(start_ws_server(params=websocket_data,
                                        output_file=os.path.join(root_data_path, "websocket", "websocket.csv"),
                                        ip=config["DATA_CAPTURE"]["WS"]["IP"],
                                        port=config["DATA_CAPTURE"]["WS"]["PORT"]))
        except asyncio.CancelledError:
            logging.warning("⚠ WebSocket server cancelled")
        except KeyboardInterrupt:
            logging.info("⚠ Stopped by user (Ctrl+C)")
        except Exception as e:
            logging.error(f"❌ Error: {e}")
    
    # Start WebSocket server in background thread
    ws_thread = threading.Thread(target=run_websocket_server, daemon=True)
    ws_thread.start()
    
    # Add protocol handler for window close
    def on_closing():
        """Handle window close event"""
        logging.info("─────────────────────────────────────────────")
        logging.info("⚠ Window closing...")
        logging.info("✓ Session completed")
        logging.info("═══════════════════════════════════════════")
        gui.destroy()
    
    gui.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Keep the GUI running and responsive
    try:
        gui.mainloop()  # This keeps the GUI window open and responsive
    except KeyboardInterrupt:
        logging.info("⚠ Stopped by user (Ctrl+C)")
        pass
