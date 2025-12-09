"""
Exercise 1: Reading CSV Files
=============================
Chapter 1: The Spreadsheet Nightmare

In this exercise, you'll practice reading CSV files using Python's csv module.
Complete the tasks below to build your CSV reading skills!

Run this file with: python exercise-1.py
"""

import csv
from pathlib import Path

# Get the path to sample data
SAMPLE_DATA = Path(__file__).parent / "sample-data"


def task_1_basic_read():
    """
    Task 1: Read a CSV file using csv.reader

    Instructions:
    1. Open 'devices.csv' from the sample-data folder
    2. Use csv.reader to read the file
    3. Print each row

    Expected output: Each row as a list
    """
    print("=" * 50)
    print("Task 1: Basic CSV Reading with csv.reader")
    print("=" * 50)

    csv_file = SAMPLE_DATA / "devices.csv"

    # YOUR CODE HERE
    # Hint: Use 'with open(csv_file, 'r') as file:' to open the file
    # Then use 'csv.reader(file)' to create a reader

    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

    print()


def task_2_dictreader():
    """
    Task 2: Read a CSV file using csv.DictReader

    Instructions:
    1. Open 'devices.csv' using DictReader
    2. Print each device's hostname and IP address

    Expected output: Device names and IPs in a formatted string
    """
    print("=" * 50)
    print("Task 2: Reading with csv.DictReader")
    print("=" * 50)

    csv_file = SAMPLE_DATA / "devices.csv"

    # YOUR CODE HERE
    # Hint: DictReader automatically uses the first row as keys

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f"Device: {row['hostname']} - IP: {row['ip_address']}")

    print()


def task_3_count_devices():
    """
    Task 3: Count devices by type

    Instructions:
    1. Read 'devices.csv'
    2. Count how many devices of each type exist
    3. Print the counts

    Expected output: A dictionary with device type counts
    """
    print("=" * 50)
    print("Task 3: Counting Devices by Type")
    print("=" * 50)

    csv_file = SAMPLE_DATA / "devices.csv"
    device_counts: dict[str, int] = {}

    # YOUR CODE HERE
    # Hint: Use a dictionary to count occurrences

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            device_type = row["device_type"]
            device_counts[device_type] = device_counts.get(device_type, 0) + 1

    print("Device counts by type:")
    for device_type, count in device_counts.items():
        print(f"  {device_type}: {count}")

    print()


def task_4_filter_devices():
    """
    Task 4: Filter devices by location

    Instructions:
    1. Read 'devices.csv'
    2. Find all devices in 'Data Center'
    3. Print their hostnames

    Expected output: List of hostnames in Data Center
    """
    print("=" * 50)
    print("Task 4: Filtering Devices by Location")
    print("=" * 50)

    csv_file = SAMPLE_DATA / "devices.csv"

    # YOUR CODE HERE

    print("Devices in Data Center:")
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["location"] == "Data Center":
                print(f"  - {row['hostname']}")

    print()


def bonus_task_interfaces():
    """
    Bonus Task: Work with related data

    Instructions:
    1. Read 'interfaces.csv'
    2. For each device, list its interfaces
    3. Print in a tree-like format

    This is more challenging - give it a try!
    """
    print("=" * 50)
    print("Bonus: Device Interfaces")
    print("=" * 50)

    csv_file = SAMPLE_DATA / "interfaces.csv"

    # Group interfaces by device
    devices: dict[str, list[dict]] = {}

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            device = row["device"]
            if device not in devices:
                devices[device] = []
            devices[device].append(row)

    # Print in tree format
    for device, interfaces in devices.items():
        print(f"📦 {device}")
        for iface in interfaces:
            ip_info = f" ({iface['ip_address']})" if iface["ip_address"] else ""
            print(f"   └── {iface['interface']}{ip_info}")

    print()


if __name__ == "__main__":
    print("\n🎓 CSV Chronicles - Exercise 1: Reading CSV Files\n")

    task_1_basic_read()
    task_2_dictreader()
    task_3_count_devices()
    task_4_filter_devices()
    bonus_task_interfaces()

    print("✅ All tasks complete! Great job!")
    print("\nNext: Try modifying the code to explore further:")
    print("  - What happens if you try to read a file that doesn't exist?")
    print("  - Can you find devices with IP addresses starting with '10.0.0'?")
    print("  - Try reading the 'devices_messy.csv' file - what issues do you see?")
