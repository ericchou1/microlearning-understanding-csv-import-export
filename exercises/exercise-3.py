"""
Exercise 3: Writing and Transforming CSV Data
==============================================
Chapter 3: Building Order from Disorder

In this exercise, you'll practice writing CSV files and building
a complete data transformation pipeline.

Run this file with: python exercise-3.py
"""

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# Get the path to sample data
SAMPLE_DATA = Path(__file__).parent / "sample-data"
OUTPUT_DIR = Path(__file__).parent / "output"


# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(exist_ok=True)


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class Device:
    """Represents a network device."""

    hostname: str
    ip_address: str
    device_type: str
    location: str
    status: str = "active"

    def to_dict(self) -> dict:
        """Convert to dictionary for CSV writing."""
        return {
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "device_type": self.device_type,
            "location": self.location,
            "status": self.status,
        }


# =============================================================================
# Normalization Functions
# =============================================================================


def normalize_hostname(hostname: str) -> str:
    """Normalize hostname: lowercase, replace underscores with dashes."""
    return hostname.lower().strip().replace("_", "-").replace(" ", "-")


def normalize_device_type(dtype: str) -> str:
    """Normalize device type to standard values."""
    type_mapping = {
        "sw": "switch",
        "switch": "switch",
        "rtr": "router",
        "router": "router",
        "fw": "firewall",
        "firewall": "firewall",
    }
    return type_mapping.get(dtype.lower().strip(), dtype.lower().strip())


def normalize_location(location: str) -> str:
    """Normalize location names."""
    location_mapping = {
        "bldg a": "building-a",
        "building a": "building-a",
        "bldg b": "building-b",
        "building b": "building-b",
        "bldg c": "building-c",
        "building c": "building-c",
        "dc": "data-center",
        "data center": "data-center",
        "datacenter": "data-center",
    }
    normalized = location.lower().strip()
    return location_mapping.get(normalized, normalized.replace(" ", "-"))


# =============================================================================
# Transformation Functions
# =============================================================================


def is_valid_row(row: dict) -> bool:
    """Check if a row has all required fields."""
    hostname = row.get("hostname", row.get("name", "")).strip()
    ip = row.get("ip", row.get("ip_address", "")).strip()
    return bool(hostname and ip)


def transform_row(row: dict) -> Optional[Device]:
    """Transform a raw CSV row into a Device object."""
    if not is_valid_row(row):
        return None

    hostname = row.get("hostname", row.get("name", "")).strip()
    ip = row.get("ip", row.get("ip_address", "")).strip()
    dtype = row.get("type", row.get("device_type", "")).strip()
    location = row.get("loc", row.get("location", "")).strip()

    return Device(
        hostname=normalize_hostname(hostname),
        ip_address=ip,
        device_type=normalize_device_type(dtype),
        location=normalize_location(location),
        status="active",
    )


# =============================================================================
# Exercise Tasks
# =============================================================================


def task_1_basic_write():
    """
    Task 1: Write a basic CSV file

    Create a CSV file with device data using csv.writer.
    """
    print("=" * 60)
    print("Task 1: Basic CSV Writing")
    print("=" * 60)

    # Sample data as lists
    devices = [
        ["switch-01", "10.0.1.1", "switch", "building-a", "active"],
        ["switch-02", "10.0.1.2", "switch", "building-a", "active"],
        ["router-core", "10.0.0.1", "router", "data-center", "active"],
    ]

    output_file = OUTPUT_DIR / "basic_output.csv"

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["hostname", "ip_address", "device_type", "location", "status"])

        # Write data rows
        writer.writerows(devices)

    print(f"✅ Created: {output_file}")
    print(f"   Rows written: {len(devices)}")
    print()


def task_2_dictwriter():
    """
    Task 2: Write CSV using DictWriter

    Create a CSV file using dictionaries for cleaner code.
    """
    print("=" * 60)
    print("Task 2: CSV Writing with DictWriter")
    print("=" * 60)

    # Sample data as dictionaries
    devices = [
        Device("firewall-main", "10.0.0.254", "firewall", "data-center"),
        Device("firewall-backup", "10.0.0.253", "firewall", "data-center"),
        Device("switch-03", "10.0.1.3", "switch", "building-b"),
    ]

    output_file = OUTPUT_DIR / "dict_output.csv"
    fieldnames = ["hostname", "ip_address", "device_type", "location", "status"]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for device in devices:
            writer.writerow(device.to_dict())

    print(f"✅ Created: {output_file}")
    print(f"   Rows written: {len(devices)}")
    print()


def task_3_transform_pipeline():
    """
    Task 3: Complete transformation pipeline

    Read messy data, transform it, and write clean output.
    """
    print("=" * 60)
    print("Task 3: Complete Transformation Pipeline")
    print("=" * 60)

    input_file = SAMPLE_DATA / "devices_messy.csv"
    output_file = OUTPUT_DIR / "cleaned_devices.csv"

    # Read and transform
    devices: list[Device] = []
    skipped = 0

    with open(input_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            device = transform_row(row)
            if device:
                devices.append(device)
            else:
                skipped += 1

    # Remove duplicates (by hostname)
    seen: set[str] = set()
    unique_devices: list[Device] = []
    duplicates = 0

    for device in devices:
        if device.hostname not in seen:
            seen.add(device.hostname)
            unique_devices.append(device)
        else:
            duplicates += 1

    # Sort by hostname
    unique_devices.sort(key=lambda d: d.hostname)

    # Write output
    fieldnames = ["hostname", "ip_address", "device_type", "location", "status"]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for device in unique_devices:
            writer.writerow(device.to_dict())

    print("📊 Transformation Results:")
    print(f"   Input file: {input_file.name}")
    print(f"   Output file: {output_file.name}")
    print(f"   Valid devices: {len(devices)}")
    print(f"   Skipped (invalid): {skipped}")
    print(f"   Duplicates removed: {duplicates}")
    print(f"   Final count: {len(unique_devices)}")
    print()


def task_4_split_by_type():
    """
    Task 4: Split devices into separate files by type

    Create separate CSV files for switches, routers, and firewalls.
    """
    print("=" * 60)
    print("Task 4: Split by Device Type")
    print("=" * 60)

    input_file = SAMPLE_DATA / "devices.csv"

    # Group devices by type
    devices_by_type: dict[str, list[dict]] = {}

    with open(input_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dtype = row["device_type"]
            if dtype not in devices_by_type:
                devices_by_type[dtype] = []
            devices_by_type[dtype].append(row)

    # Write separate files
    fieldnames = ["hostname", "ip_address", "device_type", "location"]

    for dtype, devices in devices_by_type.items():
        output_file = OUTPUT_DIR / f"{dtype}s.csv"  # Add 's' for plural

        with open(output_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(devices)

        print(f"✅ Created: {output_file.name} ({len(devices)} devices)")

    print()


def task_5_add_metadata():
    """
    Task 5: Add metadata to output

    Create a summary report file alongside the data.
    """
    print("=" * 60)
    print("Task 5: Generate Summary Report")
    print("=" * 60)

    input_file = SAMPLE_DATA / "devices.csv"
    report_file = OUTPUT_DIR / "summary_report.txt"

    # Collect statistics
    stats = {
        "total_devices": 0,
        "by_type": {},
        "by_location": {},
    }

    with open(input_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stats["total_devices"] += 1

            dtype = row["device_type"]
            stats["by_type"][dtype] = stats["by_type"].get(dtype, 0) + 1

            location = row["location"]
            stats["by_location"][location] = stats["by_location"].get(location, 0) + 1

    # Write report
    with open(report_file, "w") as file:
        file.write("=" * 50 + "\n")
        file.write("NETWORK INVENTORY SUMMARY REPORT\n")
        file.write("=" * 50 + "\n\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Source file: {input_file.name}\n\n")

        file.write(f"Total Devices: {stats['total_devices']}\n\n")

        file.write("By Device Type:\n")
        for dtype, count in sorted(stats["by_type"].items()):
            file.write(f"  - {dtype}: {count}\n")
        file.write("\n")

        file.write("By Location:\n")
        for location, count in sorted(stats["by_location"].items()):
            file.write(f"  - {location}: {count}\n")

    print(f"✅ Created: {report_file}")

    # Also print the report
    print("\n📄 Report Preview:")
    with open(report_file, "r") as file:
        print(file.read())


def show_output_files():
    """Show all files created in the output directory."""
    print("=" * 60)
    print("Output Files Created")
    print("=" * 60)

    for file in sorted(OUTPUT_DIR.iterdir()):
        size = file.stat().st_size
        print(f"  📄 {file.name} ({size} bytes)")

    print(f"\nOutput directory: {OUTPUT_DIR}")
    print()


if __name__ == "__main__":
    print("\n🎓 CSV Chronicles - Exercise 3: Writing and Transforming\n")

    task_1_basic_write()
    task_2_dictwriter()
    task_3_transform_pipeline()
    task_4_split_by_type()
    task_5_add_metadata()
    show_output_files()

    print("=" * 60)
    print("✅ All tasks complete!")
    print("=" * 60)
    print("\nChallenges to try:")
    print("  - Add a timestamp column to the output files")
    print("  - Create a 'changes' log that tracks what was modified")
    print("  - Merge data from multiple input files")
    print("  - Generate output in different formats (TSV, pipe-delimited)")
