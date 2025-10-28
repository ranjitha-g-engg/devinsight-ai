"""
Line-by-line error and issue detector
"""
import ast
import re
from typing import List, Dict


class ErrorDetector:
    """Detect errors and issues line by line"""
    
    def __init__(self):
        self.patterns = [
            {
                'pattern': r'\bif\s+[a-zA-Z_]\w*\s*=\s*(?!=)',
                'issue': 'Assignment in if condition',
                'fix': 'Use == for comparison instead of =',
                'severity': 'ERROR'
            },
            {
                'pattern': r'range\(len\(',
                'issue': 'Non-pythonic iteration',
                'fix': 'Use: for item in list instead of range(len(list))',
                'severity': 'STYLE'
            },
            {
                'pattern': r'except\s*:\s*$',
                'issue': 'Bare except clause',
                'fix': 'Specify exception type: except ValueError:',
                'severity': 'WARNING'
            },
            {
                'pattern': r'==\s*True\b|==\s*False\b',
                'issue': 'Redundant comparison to boolean',
                'fix': 'Use if variable: instead of if variable == True:',
                'severity': 'STYLE'
            },
        ]
    
    def detect_all_issues(self, code: str) -> List[Dict]:
        """Detect ONLY actual syntax errors (no false positives)"""
        issues = []
        
        # ONLY check syntax errors - these are always accurate
        syntax_issues = self.check_syntax(code)
        issues.extend(syntax_issues)
        
        # Sort by line number
        issues.sort(key=lambda x: x.get('line', 0))
        
        return issues
    
    def check_syntax(self, code: str) -> List[Dict]:
        """Check for syntax errors"""
        issues = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append({
                'line': e.lineno,
                'column': e.offset,
                'severity': 'ERROR',
                'issue': 'Syntax Error',
                'cause': e.msg,
                'code_snippet': e.text.strip() if e.text else '',
                'fix': self._get_syntax_fix(e.msg),
                'type': 'syntax'
            })
        except IndentationError as e:
            issues.append({
                'line': e.lineno,
                'column': e.offset,
                'severity': 'ERROR',
                'issue': 'Indentation Error',
                'cause': e.msg,
                'code_snippet': e.text.strip() if e.text else '',
                'fix': 'Check spacing/tabs at the beginning of the line',
                'type': 'indentation'
            })
        except Exception as e:
            issues.append({
                'line': 0,
                'severity': 'ERROR',
                'issue': 'Parsing Error',
                'cause': str(e),
                'code_snippet': '',
                'fix': 'Fix syntax errors first',
                'type': 'parsing'
            })
        
        return issues
    
    def _get_syntax_fix(self, error_msg: str) -> str:
        """Get fix suggestion based on error message"""
        fixes = {
            'invalid syntax': 'Check for missing colons, parentheses, or quotes',
            'unexpected EOF': 'Missing closing parenthesis, bracket, or quote',
            'unindent does not match': 'Fix indentation to match previous line',
            'expected an indented block': 'Add indented code after colon',
            "unterminated string": 'Add closing quote',
        }
        
        for key, fix in fixes.items():
            if key in error_msg.lower():
                return fix
        
        return 'Check syntax near this line'