
# Axiom-X Canonical Maintenance
cd "C:\Users\regan\ID SYSTEM\axiom-x"
python "C:\Users\regan\ID SYSTEM\axiom-x\continuous_canonical_validator.py"

# Send notification if duplicates found
if (Test-Path "new_duplicates_detected.json") {
    $duplicates = Get-Content "new_duplicates_detected.json" | ConvertFrom-Json
    $count = $duplicates.Count

    Write-Host "Warning: $count new duplicate files detected"
    Write-Host "Run: python safe_deletion_manager.py"
}
