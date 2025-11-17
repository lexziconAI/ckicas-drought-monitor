"""
Set up Windows Task Scheduler to run validation weekly
"""

import subprocess
from pathlib import Path

axiom_dir = Path("C:/Users/regan/ID SYSTEM/axiom-x")
validator_script = axiom_dir / "continuous_canonical_validator.py"

# Create PowerShell script for Task Scheduler
ps_script = f"""
# Axiom-X Canonical Maintenance
cd "{axiom_dir}"
python "{validator_script}"

# Send notification if duplicates found
if (Test-Path "new_duplicates_detected.json") {{
    $duplicates = Get-Content "new_duplicates_detected.json" | ConvertFrom-Json
    $count = $duplicates.Count

    Write-Host "Warning: $count new duplicate files detected"
    Write-Host "Run: python safe_deletion_manager.py"
}}
"""

ps_path = axiom_dir / "canonical_maintenance.ps1"
with open(ps_path, 'w') as f:
    f.write(ps_script)

# Create Windows Task
task_xml = f"""
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2024-11-10T09:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek>
          <Sunday />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-ExecutionPolicy Bypass -File "{ps_path}"</Arguments>
    </Exec>
  </Actions>
</Task>
"""

print("📅 SCHEDULED MAINTENANCE SETUP")
print("=" * 60)
print(f"\n1. PowerShell script created: {ps_path}")
print(f"\n2. To enable weekly automatic validation:")
print(f"\n   Run as Administrator:")
print(f'   schtasks /create /tn "Axiom-X Canonical Maintenance" /xml task.xml')
print(f"\n3. Or run manually each week:")
print(f'   python continuous_canonical_validator.py')
print("\n=" * 60)