#!/usr/bin/env python3
"""
AXIOM-X DUAL-SYSTEM MONITOR
Real-time monitoring of Phase 2 + Infrastructure Workers
Shows resource usage, throughput, and completion estimates
"""

import asyncio
import psutil
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path

class DualSystemMonitor:
    """Monitor both Phase 2 and Infrastructure systems in real-time"""

    def __init__(self):
        self.phase2_start = None
        self.infra_start = None
        self.phase2_log_file = "phase2_output.log"
        self.infra_status_file = "infrastructure_workers_status.json"

    async def monitor(self):
        """Monitor both systems in real-time"""
        print("🔍 AXIOM-X DUAL-SYSTEM TURBO MODE - LIVE DASHBOARD")
        print("=" * 80)

        # Initialize start times
        if os.path.exists(self.phase2_log_file):
            self.phase2_start = time.time()
        if os.path.exists(self.infra_status_file):
            self.infra_start = time.time()

        while True:
            # Get system resources
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()

            # Phase 2 progress
            phase2_status = self.get_phase2_status()

            # Infrastructure progress
            infra_status = self.get_infrastructure_status()

            # Display dashboard
            self.print_dashboard(cpu_percent, memory, phase2_status, infra_status)

            # Check for completion
            if phase2_status['complete'] and infra_status['complete']:
                print("\n🎉 BOTH SYSTEMS COMPLETE!")
                break

            await asyncio.sleep(5)  # Update every 5 seconds

    def get_phase2_status(self):
        """Read Phase 2 progress from log file"""
        try:
            if not os.path.exists(self.phase2_log_file):
                return {'tasks_done': 0, 'tasks_total': 1647, 'complete': False}

            with open(self.phase2_log_file, 'r') as f:
                lines = f.readlines()

            # Find latest progress
            tasks_done = 0
            tasks_total = 1647

            for line in reversed(lines):
                if 'Completed batch' in line and 'total' in line:
                    # Extract: "Completed batch 5: 250/1647 total"
                    try:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            progress_part = parts[1].strip()
                            if '/' in progress_part:
                                progress_str = progress_part.split('/')[0].strip()
                                total_str = progress_part.split('/')[1].split()[0]
                                tasks_done = int(progress_str)
                                tasks_total = int(total_str)
                                break
                    except (ValueError, IndexError):
                        continue

            complete = tasks_done >= tasks_total
            return {
                'tasks_done': tasks_done,
                'tasks_total': tasks_total,
                'complete': complete
            }

        except Exception as e:
            print(f"⚠️ Error reading Phase 2 status: {e}")
            return {'tasks_done': 0, 'tasks_total': 1647, 'complete': False}

    def get_infrastructure_status(self):
        """Read infrastructure workers progress"""
        try:
            if not os.path.exists(self.infra_status_file):
                return {'workers': 0, 'tasks_done': 0, 'complete': False}

            with open(self.infra_status_file, 'r') as f:
                data = json.load(f)

            return {
                'workers': data.get('active_workers', 0),
                'tasks_done': data.get('total_tasks_completed', 0),
                'complete': False  # Infrastructure runs continuously
            }

        except Exception as e:
            print(f"⚠️ Error reading infrastructure status: {e}")
            return {'workers': 0, 'tasks_done': 0, 'complete': False}

    def print_dashboard(self, cpu, memory, phase2, infra):
        """Print real-time dashboard"""
        # Clear screen (ANSI escape sequence)
        print("\033[H\033[J", end="")

        print("=" * 80)
        print("🚀 AXIOM-X DUAL-SYSTEM TURBO MODE - LIVE DASHBOARD")
        print("=" * 80)

        # System resources
        print("\n💻 SYSTEM RESOURCES:")
        print(f"   CPU: ████████████████  {cpu:.1f}%")
        print(f"   RAM: ████████  {memory.percent:.1f}% ({memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB)")

        # Phase 2 progress
        phase2_percent = (phase2['tasks_done'] / phase2['tasks_total']) * 100
        print("\n📊 PHASE 2 - CANONICAL FILE VALIDATION:")
        print(f"   Progress: ██████  {phase2_percent:.1f}%")
        print(f"   Tasks: {phase2['tasks_done']}/{phase2['tasks_total']}")

        # ETA for Phase 2
        if phase2['tasks_done'] > 0 and not phase2['complete']:
            tasks_remaining = phase2['tasks_total'] - phase2['tasks_done']
            # Assume 400 tasks per batch, ~60 seconds per batch
            batches_remaining = max(1, tasks_remaining / 400)
            eta_seconds = batches_remaining * 60
            eta = datetime.now() + timedelta(seconds=eta_seconds)
            print(f"   ETA: {eta.strftime('%H:%M:%S')} (~{int(eta_seconds/60)} minutes)")
        elif phase2['complete']:
            print("   Status: ✅ COMPLETE")

        # Infrastructure progress
        print("\n🔧 INFRASTRUCTURE WORKERS - NEW FEATURE BUILDING:")
        print(f"   Active Workers: {infra['workers']}")
        print(f"   Tasks Completed: {infra['tasks_done']}")
        print(f"   Status: {'🟢 Running' if infra['workers'] > 0 else '🔴 Inactive'}")

        # Performance recommendations
        print("\n💡 OPTIMIZATION TIPS:")
        if cpu < 60:
            print(f"   ⚠️  CPU usage low ({cpu:.1f}%) - Consider increasing batch sizes")
        elif cpu > 95:
            print(f"   ⚠️  CPU usage very high ({cpu:.1f}%) - System at max capacity")
        else:
            print(f"   ✅ CPU usage optimal ({cpu:.1f}%)")
        if memory.percent > 90:
            print(f"   ⚠️  Memory usage high ({memory.percent:.1f}%) - Risk of slowdown")
        else:
            print(f"   ✅ Memory usage healthy ({memory.percent:.1f}%)")
        print("=" * 80)
        print(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        print("Press Ctrl+C to stop monitoring")
        print("=" * 80)

async def main():
    """Main monitoring function"""
    monitor = DualSystemMonitor()
    try:
        await monitor.monitor()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Monitor error: {e}")

if __name__ == "__main__":
    asyncio.run(main())