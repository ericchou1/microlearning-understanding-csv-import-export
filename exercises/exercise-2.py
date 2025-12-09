"""
Exercise 2: Validating and Cleaning CSV Data
=============================================
Chapter 2: Making Sense of Chaos

In this exercise, you'll practice validating and cleaning messy CSV data.
The 'devices_messy.csv' file contains various data quality issues.

Run this file with: python exercise-2.py
"""

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Get the path to sample data
SAMPLE_DATA = Path(__file__).parent / "sample-data"


# =============================================================================
# Validation Functions
# =============================================================================


def is_valid_hostname(hostname: str) -> bool:
    """
    Check if a hostname is valid.

    Valid hostnames:
    - Not empty
    - Contains only letters, numbers, and hyphens
    - Starts and ends with alphanumeric character

    Returns: True if valid, False otherwise
    """
    if not hostname or not hostname.strip():
        return False

    # Pattern: alphanumeric, can contain hyphens, must start/end with alphanum
    pattern = r"^[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9]$|^[a-zA-Z0-9]$"
    return bool(re.match(pattern, hostname.strip()))


def is_valid_ip(ip_address: str) -> bool:
    """
    Check if an IP address is valid IPv4 format.

    Valid IPs:
    - Four octets separated by dots
    - Each octet is 0-255

    Returns: True if valid, False otherwise
    """
    if not ip_address or not ip_address.strip():
        return False

    # Check format
    pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if not re.match(pattern, ip_address.strip()):
        return False

    # Check each octet is 0-255
    octets = ip_address.strip().split(".")
    return all(0 <= int(octet) <= 255 for octet in octets)


def normalize_device_type(device_type: str) -> str:
    """
    Normalize device type to standard values.

    Maps various abbreviations to standard types:
    - sw, switch -> switch
    - rtr, router -> router
    - fw, firewall -> firewall

    Returns: Normalized device type string
    """
    type_mapping = {
        "sw": "switch",
        "switch": "switch",
        "rtr": "router",
        "router": "router",
        "fw": "firewall",
        "firewall": "firewall",
    }
    normalized = device_type.lower().strip()
    return type_mapping.get(normalized, normalized)


def normalize_location(location: str) -> str:
    """
    Normalize location names to standard values.

    Maps various location formats to standard names:
    - Bldg A, Building A -> building-a
    - DC, Data Center -> data-center

    Returns: Normalized location string
    """
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
# Data Classes
# =============================================================================


@dataclass
class ValidationResult:
    """Result of validating a single row."""

    row_number: int
    is_valid: bool
    errors: list[str]
    cleaned_data: Optional[dict] = None


# =============================================================================
# Main Validation Logic
# =============================================================================


def validate_row(row_num: int, row: dict) -> ValidationResult:
    """
    Validate a single CSV row and return results.

    Checks:
    - Hostname exists and is valid
    - IP address exists and is valid IPv4
    - Device type exists
    - Location exists

    Returns: ValidationResult with errors and cleaned data
    """
    errors = []

    # Get raw values (handle different column names)
    hostname = row.get("hostname", row.get("name", "")).strip()
    ip = row.get("ip", row.get("ip_address", "")).strip()
    device_type = row.get("type", row.get("device_type", "")).strip()
    location = row.get("loc", row.get("location", "")).strip()

    # Validate hostname
    if not hostname:
        errors.append("Missing hostname")
    elif not is_valid_hostname(hostname):
        errors.append(f"Invalid hostname format: '{hostname}'")

    # Validate IP
    if not ip:
        errors.append("Missing IP address")
    elif not is_valid_ip(ip):
        errors.append(f"Invalid IP address: '{ip}'")

    # Validate device type
    if not device_type:
        errors.append("Missing device type")

    # Validate location
    if not location:
        errors.append("Missing location")

    # Build cleaned data if no errors
    cleaned_data = None
    if not errors:
        cleaned_data = {
            "hostname": hostname.lower().replace("_", "-"),
            "ip_address": ip,
            "device_type": normalize_device_type(device_type),
            "location": normalize_location(location),
        }

    return ValidationResult(
        row_number=row_num,
        is_valid=len(errors) == 0,
        errors=errors,
        cleaned_data=cleaned_data,
    )


def process_messy_csv(input_file: Path) -> tuple[list[dict], list[ValidationResult]]:
    """
    Process a messy CSV file, validate and clean the data.

    Returns:
    - List of valid, cleaned device records
    - List of all validation results (for error reporting)
    """
    valid_devices = []
    all_results = []

    with open(input_file, "r") as file:
        reader = csv.DictReader(file)

        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            result = validate_row(row_num, row)
            all_results.append(result)

            if result.is_valid and result.cleaned_data:
                valid_devices.append(result.cleaned_data)

    return valid_devices, all_results


# =============================================================================
# Exercise Tasks
# =============================================================================


def task_1_inspect_messy_data():
    """
    Task 1: Inspect the messy data

    First, let's see what problems exist in the messy CSV file.
    """
    print("=" * 60)
    print("Task 1: Inspecting Messy Data")
    print("=" * 60)

    csv_file = SAMPLE_DATA / "devices_messy.csv"

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        print(f"Columns: {reader.fieldnames}\n")

        for row_num, row in enumerate(reader, start=2):
            print(f"Row {row_num}: {dict(row)}")

    print()


def task_2_validate_data():
    """
    Task 2: Validate the messy data

    Run validation on each row and report errors.
    """
    print("=" * 60)
    print("Task 2: Validating Data")
    print("=" * 60)

    csv_file = SAMPLE_DATA / "devices_messy.csv"
    valid_devices, results = process_messy_csv(csv_file)

    # Report errors
    print("Validation Errors:")
    print("-" * 40)
    for result in results:
        if not result.is_valid:
            print(f"⚠️  Row {result.row_number}:")
            for error in result.errors:
                print(f"     - {error}")

    print("\nSummary:")
    print(f"  Total rows: {len(results)}")
    print(f"  Valid: {len(valid_devices)}")
    print(f"  Invalid: {len(results) - len(valid_devices)}")
    print()


def task_3_show_cleaned_data():
    """
    Task 3: Show the cleaned, normalized data

    Display the valid records after cleaning and normalization.
    """
    print("=" * 60)
    print("Task 3: Cleaned Data")
    print("=" * 60)

    csv_file = SAMPLE_DATA / "devices_messy.csv"
    valid_devices, _ = process_messy_csv(csv_file)

    print("Valid devices after cleaning:\n")
    for device in valid_devices:
        print(f"  📦 {device['hostname']}")
        print(f"     IP: {device['ip_address']}")
        print(f"     Type: {device['device_type']}")
        print(f"     Location: {device['location']}")
        print()


def task_4_test_validators():
    """
    Task 4: Test the validation functions

    Try the validators with different inputs to understand how they work.
    """
    print("=" * 60)
    print("Task 4: Testing Validators")
    print("=" * 60)

    # Test hostnames
    test_hostnames = [
        "switch-01",  # Valid
        "ROUTER-CORE",  # Valid (uppercase)
        "sw_01",  # Has underscore
        "",  # Empty
        "-switch",  # Starts with dash
        "a",  # Single char (valid)
    ]

    print("Hostname Validation:")
    for hostname in test_hostnames:
        result = "✅" if is_valid_hostname(hostname) else "❌"
        print(f"  {result} '{hostname}'")

    print()

    # Test IP addresses
    test_ips = [
        "10.0.1.1",  # Valid
        "192.168.1.1",  # Valid
        "NOT_ASSIGNED",  # Invalid
        "256.1.1.1",  # Invalid (octet > 255)
        "10.0.1",  # Invalid (missing octet)
        "",  # Empty
    ]

    print("IP Address Validation:")
    for ip in test_ips:
        result = "✅" if is_valid_ip(ip) else "❌"
        print(f"  {result} '{ip}'")

    print()

    # Test normalization
    print("Device Type Normalization:")
    test_types = ["sw", "Switch", "RTR", "FW", "firewall", "unknown"]
    for dtype in test_types:
        print(f"  '{dtype}' -> '{normalize_device_type(dtype)}'")

    print()


if __name__ == "__main__":
    print("\n🎓 CSV Chronicles - Exercise 2: Validation and Cleaning\n")

    task_1_inspect_messy_data()
    task_2_validate_data()
    task_3_show_cleaned_data()
    task_4_test_validators()

    print("=" * 60)
    print("✅ All tasks complete!")
    print("=" * 60)
    print("\nChallenges to try:")
    print("  - Add validation for IP address ranges (e.g., must be in 10.x.x.x)")
    print("  - Improve hostname normalization (convert underscores to dashes)")
    print("  - Add a check for duplicate hostnames")
    print("  - Write the cleaned data to a new CSV file")
