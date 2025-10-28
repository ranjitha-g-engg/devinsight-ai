"""
Security vulnerability scanner
"""
import re
from typing import List, Dict


class SecurityScanner:
    """Scan for security issues"""
    
    def __init__(self):
        self.patterns = [
            (r'eval\(', 'HIGH', 'Dangerous eval() usage', 'Use ast.literal_eval()'),
            (r'exec\(', 'HIGH', 'Dangerous exec() usage', 'Avoid dynamic code execution'),
            (r'pickle\.loads', 'HIGH', 'Unsafe deserialization', 'Use json instead'),
            (r'os\.system', 'MEDIUM', 'Shell command execution', 'Use subprocess.run()'),
            (r'input\(', 'LOW', 'Unvalidated input', 'Validate user input'),
            (r'password\s*=\s*["\']', 'HIGH', 'Hardcoded password', 'Use environment variables'),
        ]
    
    def scan(self, code: str) -> List[Dict]:
        """Scan code for security issues"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern, severity, description, fix in self.patterns:
                if re.search(pattern, line):
                    issues.append({
                        'line': i,
                        'severity': severity,
                        'description': description,
                        'recommendation': fix,
                        'code': line.strip()
                    })
        
        return issues
    
    def get_security_score(self, issues: List[Dict]) -> int:
        """Calculate security score 0-100"""
        if not issues:
            return 100
        
        score = 100
        for issue in issues:
            if issue['severity'] == 'HIGH':
                score -= 15
            elif issue['severity'] == 'MEDIUM':
                score -= 10
            else:
                score -= 5
        
        return max(0, score)