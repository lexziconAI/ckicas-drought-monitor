"""
Script to expand infrastructure_workers_phase2.json to a larger total worker count.
Creates new worker entries named scout_NNN, extractor_NNN, validator_NNN as needed to reach target_total.
Run before starting Phase 2 or while paused.
"""
import json
from pathlib import Path

WORKERS_FILE = Path('infrastructure_workers_phase2.json')
TARGET_TOTAL = 2794

if not WORKERS_FILE.exists():
    print(f"Workers file {WORKERS_FILE} not found")
    raise SystemExit(1)

with WORKERS_FILE.open('r', encoding='utf8') as f:
    data = json.load(f)

current_total = data.get('total_workers', 0)
print(f"Current total workers: {current_total}")

if current_total >= TARGET_TOTAL:
    print("No expansion needed")
    raise SystemExit(0)

worker_status = data.get('worker_status', {})

# Determine next index
existing_ids = [int(k.split('_')[-1]) for k in worker_status.keys() if '_' in k and k.split('_')[-1].isdigit()]
next_idx = max(existing_ids) + 1 if existing_ids else 1

roles = ['scout', 'extractor', 'validator']

while len(worker_status) + 0 < TARGET_TOTAL:
    role = roles[next_idx % len(roles)]
    wid = f"{role}_{next_idx:04d}"
    worker_status[wid] = {
        'worker_id': wid,
        'status': 'active',
        'tasks_completed': 0,
        'uptime_seconds': 0.0
    }
    next_idx += 1

# Update totals
data['total_workers'] = len(worker_status)
data['active_workers'] = len(worker_status)
data['worker_status'] = worker_status

with WORKERS_FILE.open('w', encoding='utf8') as f:
    json.dump(data, f, indent=2)

print(f"Expanded workers file to {data['total_workers']} workers")
