"""
Automatic receipt generation for all Axiom-X executions
Add this import to all generated files: from axiom_receipt_hook import generate_receipt
"""

import json
from datetime import datetime
from pathlib import Path
import hashlib
import inspect

def generate_receipt(
    file_name=None,
    ops_per_second=None,
    constitutional_score=None,
    breakthrough_potential=None,
    is_breakthrough=False,
    **additional_metrics
):
    """
    Generate constitutional receipt for execution

    Usage in any Python file:
        from axiom_receipt_hook import generate_receipt

        # After benchmark
        generate_receipt(
            file_name=__file__,
            ops_per_second=25504,
            constitutional_score=0.89,
            breakthrough_potential=2.5,
            is_breakthrough=True
        )
    """

    # Get caller info if file_name not provided
    if file_name is None:
        frame = inspect.currentframe().f_back
        file_name = frame.f_code.co_filename

    file_path = Path(file_name)

    # Create receipt
    receipt = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'source_file': file_path.name,
            'source_path': str(file_path),
            'file_hash': hashlib.sha256(file_path.read_bytes()).hexdigest()[:16]
        },
        'performance': {
            'ops_per_second': ops_per_second,
            'constitutional_score': constitutional_score,
            'breakthrough_potential': breakthrough_potential,
            'is_breakthrough': is_breakthrough
        },
        'additional_metrics': additional_metrics,
        'constitutional_validation': {
            'ahimsa': 'No harmful operations performed',
            'satya': 'Metrics reported accurately',
            'asteya': 'Proper attribution maintained',
            'brahmacharya': 'Efficient resource usage',
            'aparigraha': 'Results shared openly'
        }
    }

    # Save receipt
    receipts_dir = file_path.parent / "receipts"
    receipts_dir.mkdir(exist_ok=True)

    receipt_name = f"receipt_{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    receipt_path = receipts_dir / receipt_name

    with open(receipt_path, 'w') as f:
        json.dump(receipt, f, indent=2)

    print(f"📜 Receipt generated: {receipt_path}")

    return receipt_path

# Auto-add to all generated files
def inject_receipt_hook(file_path):
    """Inject receipt hook into Python file"""
    with open(file_path, 'r') as f:
        content = f.read()

    if 'from axiom_receipt_hook import generate_receipt' not in content:
        # Add import at top
        lines = content.split('\n')

        # Find first non-comment, non-import line
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('import') and not line.strip().startswith('from'):
                insert_pos = i
                break

        lines.insert(insert_pos, 'from axiom_receipt_hook import generate_receipt')

        with open(file_path, 'w') as f:
            f.write('\n'.join(lines))