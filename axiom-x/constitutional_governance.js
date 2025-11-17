// AXIOM X CONSTITUTIONAL GOVERNANCE MODULE
// Implements Yama principles for ethical AI orchestration

class ConstitutionalGovernance {
    constructor() {
        this.principles = {
            ahimsa: {
                name: 'Ahimsa',
                meaning: 'Non-harm',
                enforcement: 'Human approval required for all deletions',
                compliance: 1.0
            },
            satya: {
                name: 'Satya',
                meaning: 'Truthfulness',
                enforcement: 'Confidence scores on all claims',
                compliance: 1.0
            },
            asteya: {
                name: 'Asteya',
                meaning: 'Non-stealing',
                enforcement: 'Proper attribution in all outputs',
                compliance: 1.0
            },
            brahmacharya: {
                name: 'Brahmacharya',
                meaning: 'Focused energy',
                enforcement: 'Efficient resource use',
                compliance: 1.0
            },
            aparigraha: {
                name: 'Aparigraha',
                meaning: 'Non-hoarding',
                enforcement: 'Automated redundancy cleanup',
                compliance: 1.0
            }
        };

        this.overallCompliance = 0.942; // 94.2% target
        this.enforcementType = 'Self-regulating with weekly validation';
    }

    // VALIDATE CONSTITUTIONAL COMPLIANCE
    validateCompliance(action, context) {
        const violations = [];
        const scores = {};

        // Check each principle
        for (const [key, principle] of Object.entries(this.principles)) {
            const score = this.evaluatePrinciple(key, action, context);
            scores[key] = score;

            if (score < 0.8) { // 80% threshold for violations
                violations.push({
                    principle: principle.name,
                    score: score,
                    reason: this.getViolationReason(key, action, context)
                });
            }
        }

        const overallScore = Object.values(scores).reduce((sum, score) => sum + score, 0) / 5;

        return {
            compliant: violations.length === 0,
            overallScore: overallScore,
            principleScores: scores,
            violations: violations,
            action: action,
            context: context,
            timestamp: new Date().toISOString()
        };
    }

    // EVALUATE INDIVIDUAL PRINCIPLE
    evaluatePrinciple(principle, action, context) {
        switch (principle) {
            case 'ahimsa':
                return this.evaluateAhimsa(action, context);
            case 'satya':
                return this.evaluateSatya(action, context);
            case 'asteya':
                return this.evaluateAsteya(action, context);
            case 'brahmacharya':
                return this.evaluateBrahmacharya(action, context);
            case 'aparigraha':
                return this.evaluateAparigraha(action, context);
            default:
                return 0.5;
        }
    }

    evaluateAhimsa(action, context) {
        // Non-harm: Check for potentially harmful actions
        const harmfulActions = ['delete', 'remove', 'destroy', 'overwrite', 'reset'];
        const hasHarmfulIntent = harmfulActions.some(word =>
            action.toLowerCase().includes(word) ||
            context.toLowerCase().includes(word)
        );

        if (hasHarmfulIntent) {
            // Require human approval for harmful actions
            return context.includes('human_approved') ? 1.0 : 0.3;
        }

        return 1.0; // No harm detected
    }

    evaluateSatya(action, context) {
        // Truthfulness: Check for confidence scores and factual claims
        const hasConfidence = context.includes('confidence') || context.includes('score');
        const hasSource = context.includes('source') || context.includes('attribution');

        let score = 0.5; // Base score
        if (hasConfidence) score += 0.3;
        if (hasSource) score += 0.2;

        return Math.min(1.0, score);
    }

    evaluateAsteya(action, context) {
        // Non-stealing: Check for proper attribution
        const hasAttribution = context.includes('attribution') ||
                              context.includes('source') ||
                              context.includes('original');

        return hasAttribution ? 1.0 : 0.4;
    }

    evaluateBrahmacharya(action, context) {
        // Focused energy: Check for efficient resource use
        const hasOptimization = context.includes('optimize') ||
                               context.includes('efficient') ||
                               context.includes('chaos');

        const hasWaste = context.includes('redundant') ||
                        context.includes('duplicate') ||
                        context.includes('excess');

        if (hasWaste && !hasOptimization) {
            return 0.3; // Waste without optimization
        }

        return hasOptimization ? 1.0 : 0.7;
    }

    evaluateAparigraha(action, context) {
        // Non-hoarding: Check for automated cleanup
        const hasCleanup = context.includes('cleanup') ||
                          context.includes('remove') ||
                          context.includes('delete') ||
                          context.includes('automated');

        const hasHoarding = context.includes('accumulate') ||
                           context.includes('store') ||
                           context.includes('keep');

        if (hasHoarding && !hasCleanup) {
            return 0.4; // Hoarding without cleanup
        }

        return hasCleanup ? 1.0 : 0.8;
    }

    getViolationReason(principle, action, context) {
        switch (principle) {
            case 'ahimsa':
                return 'Potentially harmful action requires human approval';
            case 'satya':
                return 'Missing confidence scores or source attribution';
            case 'asteya':
                return 'Insufficient attribution for intellectual property';
            case 'brahmacharya':
                return 'Inefficient resource utilization detected';
            case 'aparigraha':
                return 'Resource hoarding without cleanup mechanisms';
            default:
                return 'Unknown constitutional violation';
        }
    }

    // UPDATE COMPLIANCE SCORES
    updateCompliance(validationResult) {
        // Update individual principle compliance
        for (const [principle, score] of Object.entries(validationResult.principleScores)) {
            // Weighted average with previous compliance
            this.principles[principle].compliance =
                (this.principles[principle].compliance * 0.7) + (score * 0.3);
        }

        // Update overall compliance
        this.overallCompliance = Object.values(this.principles)
            .reduce((sum, p) => sum + p.compliance, 0) / 5;

        return {
            overallCompliance: this.overallCompliance,
            principleCompliance: Object.fromEntries(
                Object.entries(this.principles).map(([k, v]) => [k, v.compliance])
            )
        };
    }

    // GET GOVERNANCE STATUS
    getGovernanceStatus() {
        return {
            overallCompliance: this.overallCompliance,
            enforcementType: this.enforcementType,
            principles: this.principles,
            lastValidation: new Date().toISOString()
        };
    }
}

module.exports = ConstitutionalGovernance;