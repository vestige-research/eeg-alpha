#!/usr/bin/env python3
"""
Hello BrainFlow - Companion Script
===================================

Download and run this script locally to follow along with the tutorial:
https://vestige.github.io/eeg-alpha/tutorials/01-hello-brainflow.html

Requirements:
    pip install brainflow numpy

Usage:
    python 01-hello-brainflow.py

This script pauses after each step so you can follow along with the tutorial.
Press Enter to continue to the next step.
"""

import time

import numpy as np
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams

print("=" * 60)
print("Hello BrainFlow - Interactive Tutorial")
print("=" * 60)
print("\nThis script will pause after each step.")
print("Press Enter to continue to the next step.\n")
input("Press Enter to begin...")

# Step 1: Import and Initialize
board_id = BoardIds.SYNTHETIC_BOARD.value
print(f"\nStep 1: Using board ID {board_id} (SYNTHETIC_BOARD)")
input("\n[Press Enter to continue to Step 2...]")

# Step 2: Create Connection Parameters
params = BrainFlowInputParams()
print("\nStep 2: Connection parameters created")
input("\n[Press Enter to continue to Step 3...]")

# Step 3: Get Board Specifications
sampling_rate = BoardShim.get_sampling_rate(board_id)
eeg_channels = BoardShim.get_eeg_channels(board_id)

print("\nStep 3: Board specifications:")
print(f"  Sampling Rate: {sampling_rate} Hz")
print(f"  EEG Channels: {len(eeg_channels)} channels")
print(f"  Channel indices: {eeg_channels}")
input("\n[Press Enter to continue to Step 4...]")

# Step 4: Initialize and Connect
board = BoardShim(board_id, params)
print("\nStep 4: Initialize and Connect")
print("  Initializing board...")

try:
    board.prepare_session()
    print("  ✓ Connected!")
    board.start_stream()
    print("  ✓ Stream started!")
    input("\n[Press Enter to continue to Step 5...]")

    # Step 5: Collect Data
    print("\nStep 5: Collecting data for 5 seconds...")
    for i in range(5, 0, -1):
        print(f"  {i}...", flush=True)
        time.sleep(1)

    data = board.get_board_data()
    print("\n  ✓ Got data!")
    print(f"  Data shape: {data.shape}")
    print(f"  - Rows (channels): {data.shape[0]}")
    print(f"  - Columns (samples): {data.shape[1]}")
    print(f"  Expected: ~{sampling_rate * 5} samples ({sampling_rate} Hz × 5s)")
    input("\n[Press Enter to continue to Step 6...]")

    # Step 6: Examine EEG Data
    print("\nStep 6: Examining EEG data quality...")

    first_eeg_channel = eeg_channels[0]
    eeg_data = data[first_eeg_channel, :]

    print(f"\n  First EEG channel (index {first_eeg_channel}):")
    print(f"  - Mean: {np.mean(eeg_data):.2f} µV")
    print(f"  - Std Dev: {np.std(eeg_data):.2f} µV")
    print(f"  - Range: [{np.min(eeg_data):.2f}, {np.max(eeg_data):.2f}] µV")

    if np.abs(np.max(eeg_data)) < 200:
        print("\n  ✓ Values are in realistic EEG range!")
    input("\n[Press Enter to continue to Step 7...]")

    # Step 7: Understanding the Data Structure
    print("\nStep 7: Understanding the data structure...")
    print(f"  Example: First 5 samples from channel {first_eeg_channel}:")
    print(f"  {eeg_data[0:5]}")

    print("\n" + "=" * 60)
    print("Success! You've acquired your first EEG data stream!")
    print("=" * 60)
    input("\n[Press Enter to continue to Step 8 (cleanup)...]")

finally:
    # Step 8: Clean Up
    print("\nStep 8: Cleaning up...")
    board.stop_stream()
    board.release_session()
    print("  ✓ Session ended successfully")
    print("\nDone!")
