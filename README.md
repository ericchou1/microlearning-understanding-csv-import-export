# Nautobot CSV Import & Export Jobs

A practical guide to building Nautobot Jobs for CSV import and export operations.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Importing Devices from CSV](#importing-devices-from-csv)
4. [Error Handling and Idempotency](#error-handling-and-idempotency)
5. [Exporting Data to CSV](#exporting-data-to-csv)
6. [Complete Pipeline: Multi-Model Operations](#complete-pipeline-multi-model-operations)

---

## Prerequisites

This guide assumes familiarity with:

- **Python**: Functions, classes, file I/O, error handling
- **CSV operations**: Python's `csv` module, `DictReader`, `DictWriter`
- **Nautobot basics**: Data models, UI navigation, basic Job concepts

## Environment Setup

This guide uses the [100-days-of-nautobot](https://github.com/nautobot/100-days-of-nautobot) Codespace environment.

### Step 1: Launch Codespace

1. Navigate to: https://github.com/nautobot/100-days-of-nautobot
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for the Codespace to build

### Step 2: Start Nautobot

```bash
cd nautobot-docker-compose/
poetry shell
invoke build      # First time only
invoke db-import  # First time only
invoke debug
```

**Restarting an existing Codespace:**

```bash
cd nautobot-docker-compose/
poetry shell
invoke debug
```

### Step 3: Access Nautobot

- **URL**: The forwarded port URL shown by Codespaces (port 8080)
- **Credentials**: `admin` / `admin`

---

## Importing Devices from CSV

### CSV Structure

The sample file `data/devices.csv`:

```csv
hostname,device_type,role,location
tn-sw-01,Catalyst 9300,Access Switch,TechNova HQ
tn-sw-02,Catalyst 9300,Access Switch,TechNova HQ
tn-rtr-core,ASR 1001-X,Core Router,TechNova DC
```

### Basic Import Job

Create a file `jobs/device_import.py`:

```python
import csv
from io import StringIO

from nautobot.apps.jobs import Job, register_jobs, FileVar
from nautobot.dcim.models import Device, DeviceType, Location
from nautobot.extras.models import Role, Status


class DeviceCSVImport(Job):
    """Import devices from a CSV file into Nautobot."""
    
    class Meta:
        name = "Device CSV Import"
        description = "Upload a CSV file to import devices"
    
    csv_file = FileVar(
        description="CSV file with columns: hostname, device_type, role, location"
    )
    
    def run(self, csv_file):
        # Read and decode the file
        file_content = csv_file.read().decode('utf-8')
        self.logger.info("Processing CSV file...")
        
        # Parse CSV using StringIO to treat string as file
        reader = csv.DictReader(StringIO(file_content))
        
        # Get the Active status once (reuse for all devices)
        active_status = Status.objects.get(name="Active")
        
        # Track results
        created_count = 0
        error_count = 0
        
        for row_num, row in enumerate(reader, start=2):
            # Extract fields from CSV row
            hostname = row.get('hostname', '').strip()
            device_type_name = row.get('device_type', '').strip()
            role_name = row.get('role', '').strip()
            location_name = row.get('location', '').strip()
            
            # Skip empty rows
            if not hostname:
                continue
            
            # Look up DeviceType
            try:
                device_type = DeviceType.objects.get(model=device_type_name)
            except DeviceType.DoesNotExist:
                self.logger.warning(f"Row {row_num}: DeviceType '{device_type_name}' not found")
                error_count += 1
                continue
            
            # Look up Role
            try:
                role = Role.objects.get(name=role_name)
            except Role.DoesNotExist:
                self.logger.warning(f"Row {row_num}: Role '{role_name}' not found")
                error_count += 1
                continue
            
            # Look up Location
            try:
                location = Location.objects.get(name=location_name)
            except Location.DoesNotExist:
                self.logger.warning(f"Row {row_num}: Location '{location_name}' not found")
                error_count += 1
                continue
            
            # Create the device
            try:
                device = Device(
                    name=hostname,
                    device_type=device_type,
                    role=role,
                    location=location,
                    status=active_status,
                )
                device.validated_save()
                self.logger.info(f"✅ Created: {hostname}")
                created_count += 1
                
            except Exception as e:
                self.logger.error(f"Row {row_num}: Failed to create {hostname}: {e}")
                error_count += 1
        
        # Summary
        self.logger.info("=" * 50)
        self.logger.info(f"Import Complete!")
        self.logger.info(f"  Created: {created_count}")
        self.logger.info(f"  Errors: {error_count}")
        
        return f"Created {created_count} devices, {error_count} errors"


register_jobs(DeviceCSVImport)
```

### Key Concepts

| Component | Purpose |
|-----------|---------|
| `FileVar` | Creates a file upload field in the Job UI |
| `StringIO` | Wraps a string so `csv.DictReader` can treat it as a file |
| `validated_save()` | Validates data before saving (preferred over `save()`) |
| `self.logger` | Logs messages to the Job output in the UI |

### Running the Job

1. Navigate to **Jobs → Jobs** in Nautobot
2. Find your Job and click **Edit**
3. Check **Enabled** and click **Save**
4. Click the Job name, then **Run**
5. Upload your CSV file and click **Run Job**

---

## Error Handling and Idempotency

### The Problem

Running the import twice causes errors:

```
ERROR | UNIQUE constraint failed: dcim_device.name
```

Devices already exist from the first run!

### Solution: get_or_create

Django's `get_or_create()` either retrieves an existing object or creates a new one:

```python
# Returns (object, created_boolean)
device, created = Device.objects.get_or_create(
    name=hostname,  # Lookup field
    defaults={      # Fields set only when creating
        "device_type": device_type,
        "role": role,
        "location": location,
        "status": active_status,
    }
)

if created:
    self.logger.info(f"✅ Created: {hostname}")
    created_count += 1
else:
    self.logger.info(f"⏭️  Skipped (exists): {hostname}")
    skipped_count += 1
```

### update_or_create

If you want to update existing records with new data:

```python
device, created = Device.objects.update_or_create(
    name=hostname,  # Lookup field
    defaults={      # Fields to set (create or update)
        "device_type": device_type,
        "role": role,
        "location": location,
        "status": active_status,
    }
)

if created:
    self.logger.info(f"✅ Created: {hostname}")
else:
    self.logger.info(f"🔄 Updated: {hostname}")
```

### Comparison

| Method | If Object Exists | Use When |
|--------|------------------|----------|
| `get_or_create` | Returns as-is | Don't overwrite local changes |
| `update_or_create` | Updates fields | CSV is source of truth |

### Complete Robust Import Job

```python
import csv
from io import StringIO

from nautobot.apps.jobs import Job, register_jobs, FileVar, BooleanVar
from nautobot.dcim.models import Device, DeviceType, Location, LocationType
from nautobot.extras.models import Role, Status


class DeviceCSVImportRobust(Job):
    """Idempotent CSV import with error handling."""
    
    class Meta:
        name = "Device CSV Import (Robust)"
        description = "Safe to run multiple times"
    
    csv_file = FileVar(description="CSV file to import")
    
    update_existing = BooleanVar(
        description="Update existing devices instead of skipping",
        default=False
    )
    
    def run(self, csv_file, update_existing):
        content = csv_file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        
        active_status = Status.objects.get(name="Active")
        default_loc_type = LocationType.objects.first()
        
        created, updated, skipped, errors = 0, 0, 0, []
        
        for row_num, row in enumerate(reader, start=2):
            hostname = row.get('hostname', '').strip()
            if not hostname:
                continue
            
            device_type_name = row.get('device_type', '').strip()
            role_name = row.get('role', '').strip()
            location_name = row.get('location', '').strip()
            
            # Look up DeviceType (required)
            try:
                device_type = DeviceType.objects.get(model=device_type_name)
            except DeviceType.DoesNotExist:
                errors.append(f"Row {row_num}: DeviceType '{device_type_name}' not found")
                continue
            
            # Look up Role (required)
            try:
                role = Role.objects.get(name=role_name)
            except Role.DoesNotExist:
                errors.append(f"Row {row_num}: Role '{role_name}' not found")
                continue
            
            # Get or create Location (auto-create if missing)
            location, _ = Location.objects.get_or_create(
                name=location_name,
                defaults={
                    "location_type": default_loc_type,
                    "status": active_status,
                }
            )
            
            # Create or update device
            try:
                if update_existing:
                    device, was_created = Device.objects.update_or_create(
                        name=hostname,
                        defaults={
                            "device_type": device_type,
                            "role": role,
                            "location": location,
                            "status": active_status,
                        }
                    )
                    if was_created:
                        created += 1
                    else:
                        updated += 1
                else:
                    device, was_created = Device.objects.get_or_create(
                        name=hostname,
                        defaults={
                            "device_type": device_type,
                            "role": role,
                            "location": location,
                            "status": active_status,
                        }
                    )
                    if was_created:
                        created += 1
                    else:
                        skipped += 1
                        
            except Exception as e:
                errors.append(f"Row {row_num}: {hostname} - {e}")
        
        # Log summary
        self.logger.info("=" * 50)
        self.logger.info(f"Created: {created}, Updated: {updated}, Skipped: {skipped}, Errors: {len(errors)}")
        
        for error in errors[:10]:
            self.logger.warning(error)
        
        return f"Created: {created}, Updated: {updated}, Skipped: {skipped}, Errors: {len(errors)}"


register_jobs(DeviceCSVImportRobust)
```

---

## Exporting Data to CSV

### Querying Nautobot Data

Django's QuerySet API retrieves data efficiently:

```python
from nautobot.dcim.models import Device

# Get all devices
all_devices = Device.objects.all()

# Filter by location
dc_devices = Device.objects.filter(location__name="Data Center")

# Filter by multiple criteria
active_switches = Device.objects.filter(
    role__name="Access Switch",
    status__name="Active"
)

# Order results
devices_sorted = Device.objects.all().order_by('name')

# Optimize with select_related (for ForeignKey fields)
devices = Device.objects.select_related(
    'device_type',
    'location',
    'role',
    'status'
).all()
```

### Basic Export Job

```python
import csv
from io import StringIO

from nautobot.apps.jobs import Job, register_jobs, ObjectVar
from nautobot.dcim.models import Device, Location


class DeviceCSVExport(Job):
    """Export devices to CSV format."""
    
    class Meta:
        name = "Device CSV Export"
        description = "Generate a CSV report of devices"
    
    location = ObjectVar(
        model=Location,
        required=False,
        description="Filter by location (leave empty for all)"
    )
    
    def run(self, location=None):
        # Build the query with related data
        queryset = Device.objects.select_related(
            'device_type__manufacturer',
            'location',
            'role',
            'status'
        )
        
        # Apply filter if provided
        if location:
            queryset = queryset.filter(location=location)
        
        queryset = queryset.order_by('name')
        
        # Create CSV output
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'hostname', 'device_type', 'manufacturer',
            'role', 'location', 'status'
        ])
        
        # Write data rows
        for device in queryset:
            writer.writerow([
                device.name,
                device.device_type.model,
                device.device_type.manufacturer.name,
                device.role.name if device.role else '',
                device.location.name if device.location else '',
                device.status.name if device.status else '',
            ])
        
        csv_content = output.getvalue()
        
        # Log preview
        self.logger.info(f"Generated CSV with {queryset.count()} devices")
        self.logger.info("=" * 50)
        for line in csv_content.split('\n')[:10]:
            self.logger.info(line)
        
        return f"Exported {queryset.count()} devices"


register_jobs(DeviceCSVExport)
```

### Job Variable Types

| Variable | Purpose | UI Element |
|----------|---------|------------|
| `FileVar` | File upload | File picker |
| `ObjectVar` | Single object selection | Dropdown |
| `MultiObjectVar` | Multiple object selection | Multi-select |
| `StringVar` | Text input | Text field |
| `BooleanVar` | True/False | Checkbox |
| `ChoiceVar` | Predefined choices | Dropdown |

### IP Address Export Example

```python
import csv
from io import StringIO

from nautobot.apps.jobs import Job, register_jobs
from nautobot.ipam.models import IPAddress


class IPAddressExport(Job):
    """Export IP addresses with assignments."""
    
    class Meta:
        name = "IP Address Export"
    
    def run(self):
        queryset = IPAddress.objects.select_related(
            'status', 'parent'
        ).prefetch_related(
            'interfaces', 'interfaces__device'
        ).order_by('host')
        
        output = StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            'ip_address', 'prefix', 'status',
            'assigned_device', 'assigned_interface'
        ])
        
        for ip in queryset:
            interface = ip.interfaces.first() if ip.interfaces.exists() else None
            device_name = interface.device.name if interface and interface.device else ''
            interface_name = interface.name if interface else ''
            
            writer.writerow([
                str(ip.address),
                str(ip.parent) if ip.parent else '',
                ip.status.name if ip.status else '',
                device_name,
                interface_name,
            ])
        
        self.logger.info(f"Exported {queryset.count()} IP addresses")
        return f"Exported {queryset.count()} IP addresses"


register_jobs(IPAddressExport)
```

### select_related vs prefetch_related

| Method | Use For | Example |
|--------|---------|---------|
| `select_related` | ForeignKey, OneToOne | `device.location` |
| `prefetch_related` | ManyToMany, reverse FK | `ip.interfaces.all()` |

---

## Complete Pipeline: Multi-Model Operations

### Import Order

When importing related data, order matters:

1. **Prefixes** (IP ranges) - no dependencies
2. **Devices** - requires DeviceType, Role, Location
3. **Interfaces** - requires Device
4. **IP Addresses** - requires Interface (for assignment)

### Prefix Import

```python
import csv
from io import StringIO

from nautobot.apps.jobs import Job, register_jobs, FileVar
from nautobot.ipam.models import Prefix, Namespace
from nautobot.extras.models import Status


class PrefixImport(Job):
    class Meta:
        name = "Prefix CSV Import"
    
    csv_file = FileVar(description="CSV with: prefix, namespace, status, description")
    
    def run(self, csv_file):
        content = csv_file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        
        active_status = Status.objects.get(name="Active")
        created = 0
        
        for row in reader:
            prefix_str = row.get('prefix', '').strip()
            namespace_name = row.get('namespace', 'Global').strip()
            description = row.get('description', '').strip()
            
            if not prefix_str:
                continue
            
            namespace, _ = Namespace.objects.get_or_create(name=namespace_name)
            
            prefix, was_created = Prefix.objects.get_or_create(
                prefix=prefix_str,
                namespace=namespace,
                defaults={
                    "status": active_status,
                    "description": description,
                }
            )
            
            if was_created:
                created += 1
        
        return f"Created {created} prefixes"


register_jobs(PrefixImport)
```

### Interface Import

```python
import csv
from io import StringIO

from nautobot.apps.jobs import Job, register_jobs, FileVar
from nautobot.dcim.models import Device, Interface
from nautobot.extras.models import Status


class InterfaceImport(Job):
    class Meta:
        name = "Interface CSV Import"
    
    csv_file = FileVar(description="CSV with: device, name, type, enabled, description")
    
    def run(self, csv_file):
        content = csv_file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        
        active_status = Status.objects.get(name="Active")
        created, errors = 0, 0
        
        for row_num, row in enumerate(reader, start=2):
            device_name = row.get('device', '').strip()
            interface_name = row.get('name', '').strip()
            interface_type = row.get('type', '1000base-t').strip()
            enabled = row.get('enabled', 'true').lower() == 'true'
            description = row.get('description', '').strip()
            
            if not device_name or not interface_name:
                continue
            
            try:
                device = Device.objects.get(name=device_name)
            except Device.DoesNotExist:
                self.logger.warning(f"Row {row_num}: Device '{device_name}' not found")
                errors += 1
                continue
            
            interface, was_created = Interface.objects.get_or_create(
                device=device,
                name=interface_name,
                defaults={
                    "type": interface_type,
                    "enabled": enabled,
                    "description": description,
                    "status": active_status,
                }
            )
            
            if was_created:
                created += 1
        
        return f"Created {created} interfaces, {errors} errors"


register_jobs(InterfaceImport)
```

### IP Address Import with Interface Assignment

```python
import csv
from io import StringIO

from nautobot.apps.jobs import Job, register_jobs, FileVar
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import IPAddress, Namespace
from nautobot.extras.models import Status


class IPAddressImport(Job):
    class Meta:
        name = "IP Address CSV Import"
    
    csv_file = FileVar(description="CSV with: ip_address, device, interface, description")
    
    def run(self, csv_file):
        content = csv_file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        
        active_status = Status.objects.get(name="Active")
        namespace = Namespace.objects.get(name="Global")
        
        created, assigned, errors = 0, 0, 0
        
        for row_num, row in enumerate(reader, start=2):
            ip_str = row.get('ip_address', '').strip()
            device_name = row.get('device', '').strip()
            interface_name = row.get('interface', '').strip()
            description = row.get('description', '').strip()
            
            if not ip_str:
                continue
            
            # Get or create IP address
            ip_address, was_created = IPAddress.objects.get_or_create(
                address=ip_str,
                namespace=namespace,
                defaults={
                    "status": active_status,
                    "description": description,
                }
            )
            
            if was_created:
                created += 1
            
            # Assign to interface if specified
            if device_name and interface_name:
                try:
                    device = Device.objects.get(name=device_name)
                    interface = Interface.objects.get(device=device, name=interface_name)
                    
                    # Add IP to interface (M2M relationship)
                    if ip_address not in interface.ip_addresses.all():
                        interface.ip_addresses.add(ip_address)
                        assigned += 1
                        
                except (Device.DoesNotExist, Interface.DoesNotExist) as e:
                    self.logger.warning(f"Row {row_num}: {e}")
                    errors += 1
        
        return f"Created {created} IPs, assigned {assigned}, {errors} errors"


register_jobs(IPAddressImport)
```

### Full Network Export

```python
import csv
from io import StringIO

from nautobot.apps.jobs import Job, register_jobs, ObjectVar
from nautobot.dcim.models import Device, Location


class FullNetworkExport(Job):
    """Export devices with interfaces and IPs."""
    
    class Meta:
        name = "Full Network Export"
    
    location = ObjectVar(model=Location, required=False)
    
    def run(self, location=None):
        queryset = Device.objects.select_related(
            'device_type__manufacturer', 'location', 'role', 'status'
        ).prefetch_related(
            'interfaces', 'interfaces__ip_addresses'
        ).order_by('name')
        
        if location:
            queryset = queryset.filter(location=location)
        
        output = StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            'device', 'device_type', 'location',
            'interface', 'interface_type', 'ip_address'
        ])
        
        row_count = 0
        for device in queryset:
            for interface in device.interfaces.all():
                ips = interface.ip_addresses.all()
                if ips:
                    for ip in ips:
                        writer.writerow([
                            device.name,
                            device.device_type.model,
                            device.location.name if device.location else '',
                            interface.name,
                            interface.type,
                            str(ip.address)
                        ])
                        row_count += 1
                else:
                    writer.writerow([
                        device.name,
                        device.device_type.model,
                        device.location.name if device.location else '',
                        interface.name,
                        interface.type,
                        ''
                    ])
                    row_count += 1
        
        self.logger.info(f"Exported {row_count} rows")
        return f"Exported {row_count} rows from {queryset.count()} devices"


register_jobs(FullNetworkExport)
```

---

## Sample Data

Sample CSV files are included in the `data/` directory:

- `devices.csv` - Device inventory
- `interfaces.csv` - Device interfaces
- `ip_addresses.csv` - IP address assignments
- `prefixes.csv` - IP prefixes/subnets

---

## Resources

- [Nautobot Documentation](https://docs.nautobot.com/)
- [Nautobot Jobs Guide](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/jobs/)
- [100 Days of Nautobot](https://github.com/nautobot/100-days-of-nautobot)
- [Day 22: Process CSV Files](https://github.com/nautobot/100-days-of-nautobot/tree/main/Day022_Process_CSV_Files)

## License

MIT License
