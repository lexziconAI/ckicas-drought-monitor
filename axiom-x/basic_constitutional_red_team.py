#!/usr/bin/env python3
"""
Basic Constitutional AI Security Analysis Tool
Performs security assessment of the Constitutional Market Harmonics Dashboard
"""

import json
import requests
import time
from typing import Dict, List, Any
import hashlib
import re

class ConstitutionalSecurityAnalyzer:
    """Security analyzer for Constitutional AI systems"""

    def __init__(self, target_url: str = "http://localhost:10000"):
        self.target_url = target_url
        self.findings = []
        self.constitutional_principles = {
            "ahimsa": "Non-violence in code and operations",
            "satya": "Truthfulness in data and responses",
            "asteya": "Non-stealing of computational resources",
            "brahmacharya": "Conservation of system integrity",
            "aparigraha": "Non-attachment to unnecessary complexity"
        }

    def analyze_endpoint_security(self) -> Dict[str, Any]:
        """Analyze basic endpoint security"""
        findings = []

        try:
            # Test basic connectivity
            response = requests.get(self.target_url, timeout=10)
            findings.append({
                "test": "Basic Connectivity",
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "details": f"Status Code: {response.status_code}",
                "constitutional_compliance": "satya"
            })

            # Check for security headers
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Content-Security-Policy',
                'Strict-Transport-Security'
            ]

            missing_headers = []
            for header in security_headers:
                if header not in response.headers:
                    missing_headers.append(header)

            if missing_headers:
                findings.append({
                    "test": "Security Headers",
                    "status": "WARN",
                    "details": f"Missing headers: {', '.join(missing_headers)}",
                    "constitutional_compliance": "brahmacharya"
                })
            else:
                findings.append({
                    "test": "Security Headers",
                    "status": "PASS",
                    "details": "All security headers present",
                    "constitutional_compliance": "brahmacharya"
                })

        except requests.exceptions.RequestException as e:
            findings.append({
                "test": "Basic Connectivity",
                "status": "FAIL",
                "details": f"Connection error: {str(e)}",
                "constitutional_compliance": "satya"
            })

        return {"endpoint_security": findings}

    def analyze_constitutional_compliance(self) -> Dict[str, Any]:
        """Analyze constitutional AI compliance"""
        findings = []

        # Check for chaos optimization indicators
        chaos_indicators = [
            "lorenz", "chen", "rossler", "fractal", "attractor"
        ]

        try:
            response = requests.get(self.target_url, timeout=10)
            content = response.text.lower()

            chaos_found = []
            for indicator in chaos_indicators:
                if indicator in content:
                    chaos_found.append(indicator)

            if chaos_found:
                findings.append({
                    "test": "Chaos Theory Integration",
                    "status": "PASS",
                    "details": f"Found chaos indicators: {', '.join(chaos_found)}",
                    "constitutional_compliance": "aparigraha"
                })
            else:
                findings.append({
                    "test": "Chaos Theory Integration",
                    "status": "WARN",
                    "details": "No chaos theory indicators detected in response",
                    "constitutional_compliance": "aparigraha"
                })

        except Exception as e:
            findings.append({
                "test": "Chaos Theory Integration",
                "status": "ERROR",
                "details": f"Analysis failed: {str(e)}",
                "constitutional_compliance": "aparigraha"
            })

        return {"constitutional_compliance": findings}

    def analyze_authentication_security(self) -> Dict[str, Any]:
        """Analyze authentication mechanisms"""
        findings = []

        # Test login endpoint
        login_url = f"{self.target_url}/login"
        try:
            response = requests.post(login_url,
                                   json={"password": "test"},
                                   timeout=10)

            if response.status_code == 401:
                findings.append({
                    "test": "Authentication Rejection",
                    "status": "PASS",
                    "details": "Properly rejects invalid credentials",
                    "constitutional_compliance": "asteya"
                })
            elif response.status_code == 200:
                findings.append({
                    "test": "Authentication Security",
                    "status": "FAIL",
                    "details": "Accepts invalid credentials - SECURITY RISK",
                    "constitutional_compliance": "asteya"
                })
            else:
                findings.append({
                    "test": "Authentication Response",
                    "status": "INFO",
                    "details": f"Unexpected status: {response.status_code}",
                    "constitutional_compliance": "asteya"
                })

        except requests.exceptions.RequestException:
            findings.append({
                "test": "Authentication Endpoint",
                "status": "ERROR",
                "details": "Login endpoint not accessible",
                "constitutional_compliance": "asteya"
            })

        return {"authentication_security": findings}

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        print("🔒 CONSTITUTIONAL AI SECURITY ANALYSIS")
        print("=" * 50)

        all_findings = []

        # Run all analyses
        endpoint_results = self.analyze_endpoint_security()
        constitutional_results = self.analyze_constitutional_compliance()
        auth_results = self.analyze_authentication_security()

        # Combine results
        all_results = {**endpoint_results, **constitutional_results, **auth_results}

        # Calculate compliance score
        total_tests = 0
        passed_tests = 0

        for category, tests in all_results.items():
            print(f"\n📋 {category.replace('_', ' ').title()}:")
            for test in tests:
                status_icon = {
                    "PASS": "✅",
                    "FAIL": "❌",
                    "WARN": "⚠️",
                    "ERROR": "🔥",
                    "INFO": "ℹ️"
                }.get(test["status"], "❓")

                print(f"  {status_icon} {test['test']}: {test['details']}")

                total_tests += 1
                if test["status"] == "PASS":
                    passed_tests += 1

                all_findings.append(test)

        # Calculate constitutional compliance
        compliance_score = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        print(f"\n🎯 OVERALL CONSTITUTIONAL COMPLIANCE: {compliance_score:.1f}%")
        print(f"   Tests Passed: {passed_tests}/{total_tests}")

        # Generate recommendations
        recommendations = []
        if compliance_score < 80:
            recommendations.append("Implement missing security headers")
            recommendations.append("Strengthen authentication mechanisms")
            recommendations.append("Add chaos theory optimization layers")

        if recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"   • {rec}")

        return {
            "timestamp": time.time(),
            "target": self.target_url,
            "compliance_score": compliance_score,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "findings": all_findings,
            "recommendations": recommendations
        }

def main():
    """Main execution function"""
    analyzer = ConstitutionalSecurityAnalyzer()

    try:
        report = analyzer.generate_report()

        # Save report
        with open("constitutional_security_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print("\n📄 Report saved: constitutional_security_report.json")
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()