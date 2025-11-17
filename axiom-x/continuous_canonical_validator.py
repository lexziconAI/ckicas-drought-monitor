"""
Runs periodically (daily/weekly) to detect new duplicates and flag for cleanup
"""

import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

class ContinuousCanonicalValidator:
    def __init__(self, axiom_dir):
        self.axiom_dir = Path(axiom_dir)
        self.canonical_map_path = self.axiom_dir / "validated_canonical_map.json"

    def detect_new_duplicates(self):
        """Find files created since last validation"""

        # Load current canonical map
        with open(self.canonical_map_path, 'r') as f:
            canonical_data = json.load(f)

        canonical_files = set()
        for full_path in canonical_data.keys():
            filename = Path(full_path).name
            canonical_files.add(filename)

        # Find Python files
        all_py_files = list(self.axiom_dir.rglob("*.py"))

        # Group by base name
        file_groups = defaultdict(list)
        for py_file in all_py_files:
            if '__pycache__' in str(py_file):
                continue

            base = py_file.stem
            for pattern in ['_v1', '_v2', '_v3', '_draft', '_old', '_new']:
                if pattern in base:
                    base = base.split(pattern)[0]
                    break

            file_groups[base].append(py_file)

        # Find groups with potential duplicates
        new_duplicates = []
        for base, files in file_groups.items():
            if len(files) > 1:
                # Check if canonical version exists
                canonical_versions = [f for f in files if f.name in canonical_files]

                if canonical_versions:
                    canonical = canonical_versions[0]
                    for f in files:
                        if f != canonical:
                            # Check if created recently (within 7 days)
                            created = datetime.fromtimestamp(f.stat().st_ctime)
                            if datetime.now() - created < timedelta(days=7):
                                new_duplicates.append({
                                    'file': str(f),
                                    'name': f.name,
                                    'canonical_alternative': canonical.name,
                                    'created': created.isoformat(),
                                    'status': 'needs_validation'
                                })

        return new_duplicates

    def check_new_receipts(self):
        """Find new receipt files to update canonical map"""

        receipts_dir = self.axiom_dir / "receipts"
        if not receipts_dir.exists():
            return []

        # Find receipts created in last 7 days
        recent_receipts = []
        for receipt_file in receipts_dir.glob("receipt_*.json"):
            created = datetime.fromtimestamp(receipt_file.stat().st_ctime)
            if datetime.now() - created < timedelta(days=7):
                try:
                    with open(receipt_file, 'r') as f:
                        data = json.load(f)
                    recent_receipts.append(data)
                except:
                    pass

        return recent_receipts

    def update_canonical_map(self, new_receipts):
        """Update canonical map with new performance data"""

        # Load current map
        with open(self.canonical_map_path, 'r') as f:
            canonical_data = json.load(f)

        # Process new receipts
        updates_made = 0
        for receipt in new_receipts:
            source_file = receipt.get('metadata', {}).get('source_file')
            perf = receipt.get('performance', {})

            if source_file and perf:
                # Find the full path for this file
                file_full_path = None
                for existing_path in canonical_data.keys():
                    if Path(existing_path).name == source_file:
                        file_full_path = existing_path
                        break

                if file_full_path:
                    # Update existing entry
                    file_data = canonical_data[file_full_path]

                    # Calculate breakthrough score
                    breakthrough_score = 0
                    if perf.get('is_breakthrough'):
                        breakthrough_score += 100
                    if perf.get('ops_per_second', 0) > 10000:
                        breakthrough_score += 50
                    if perf.get('constitutional_score', 0) > 0.85:
                        breakthrough_score += 30

                    if breakthrough_score > file_data.get('breakthrough_potential', 0):
                        file_data['breakthrough_potential'] = breakthrough_score
                        file_data.update(perf)
                        updates_made += 1

        # Save updated map
        if updates_made > 0:
            with open(self.canonical_map_path, 'w') as f:
                json.dump(canonical_data, f, indent=2)

        return updates_made

    def run_validation_cycle(self):
        """Complete validation cycle"""
        print("🔄 CONTINUOUS CANONICAL VALIDATION")
        print("=" * 60)

        # Check for new duplicates
        print("\n🔍 Checking for new duplicate files...")
        new_dups = self.detect_new_duplicates()
        print(f"   Found {len(new_dups)} potential duplicates")

        if new_dups:
            print("\n⚠️  New duplicates detected:")
            for dup in new_dups[:10]:
                print(f"   • {dup['name']} (→ keep {dup['canonical_alternative']})")

            # Save for review
            with open('new_duplicates_detected.json', 'w') as f:
                json.dump(new_dups, f, indent=2)
            print(f"\n💾 Full list saved to: new_duplicates_detected.json")

        # Check for new receipts
        print("\n🔍 Checking for new performance receipts...")
        new_receipts = self.check_new_receipts()
        print(f"   Found {len(new_receipts)} new receipts")

        # Update canonical map
        if new_receipts:
            print("\n📊 Updating canonical map...")
            updates = self.update_canonical_map(new_receipts)
            print(f"   Updated {updates} entries")

        print("\n✅ Validation cycle complete")
        print("=" * 60)

# Run validator
if __name__ == "__main__":
    validator = ContinuousCanonicalValidator("C:/Users/regan/ID SYSTEM/axiom-x")
    validator.run_validation_cycle()