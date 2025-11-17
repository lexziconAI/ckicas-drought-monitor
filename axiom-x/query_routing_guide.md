# Claude Knowledge Base Query Routing Guide

Generated: 2025-11-05T17:54:10.092386
Knowledge Cutoff: 2023-08-01

## Routing Recommendations

### Internal Knowledge Only (High Confidence >= 0.85)
Use Claude's internal knowledge without external search:

- **philosophy.ethics**: comprehensive coverage, 0.95 confidence
- **philosophy.metaphysics**: extensive coverage, 0.90 confidence
- **science.physics**: comprehensive coverage, 0.95 confidence
- **science.biology**: extensive coverage, 0.90 confidence
- **science.computer_science**: comprehensive coverage, 0.95 confidence
- **technology.artificial_intelligence**: comprehensive coverage, 0.98 confidence
- **technology.software_development**: extensive coverage, 0.92 confidence
- **law.constitutional_law**: extensive coverage, 0.88 confidence

### Internal Preferred (Medium Confidence 0.70-0.85)
Use internal knowledge but consider verification:

- **law.technology_law**: moderate coverage, 0.75 confidence

### External Search Required (Low Confidence < 0.70)
Prioritize external sources:

- **current_events**: limited coverage, 0.30 confidence

## Temporal Considerations

- Knowledge cutoff: 2023-08-01
- Confidence decay: 10.0% per year
- Recent events (2024+) have significantly reduced confidence

## Recommended External Sources

- academic databases
- specialized journals
- expert consultations
- recent publications
- news archives
- current research papers
