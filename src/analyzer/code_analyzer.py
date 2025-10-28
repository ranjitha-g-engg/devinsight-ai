"""
DevInsight AI - Core Code Analyzer
"""
import ast
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class FunctionInfo:
    name: str
    line_number: int
    args: List[str]
    docstring: Optional[str]
    complexity: int
    lines: int
    
    def to_dict(self):
        return asdict(self)


@dataclass
class CodeMetrics:
    total_lines: int
    code_lines: int
    functions_count: int
    classes_count: int
    complexity_score: int
    
    def to_dict(self):
        return asdict(self)


class CodeAnalyzer:
    """Analyze Python code structure and quality"""
    
    def analyze(self, code: str) -> Dict:
        """Main analysis function"""
        try:
            tree = ast.parse(code)
            
            functions = self._extract_functions(tree)
            classes = self._extract_classes(tree)
            imports = self._extract_imports(tree)
            metrics = self._calculate_metrics(code, tree)
            suggestions = self._generate_suggestions(functions, classes, code)
            skill_gaps = self._detect_skill_gaps(code, functions, classes)
            
            return {
                'success': True,
                'functions': [f.to_dict() for f in functions],
                'classes': classes,
                'imports': imports,
                'metrics': metrics.to_dict(),
                'suggestions': suggestions,
                'skill_gaps': skill_gaps
            }
            
        except SyntaxError as e:
            return {
                'success': False,
                'error': f"Syntax Error on line {e.lineno}: {e.msg}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_functions(self, tree) -> List[FunctionInfo]:
        """Extract all functions"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(FunctionInfo(
                    name=node.name,
                    line_number=node.lineno,
                    args=[arg.arg for arg in node.args.args],
                    docstring=ast.get_docstring(node),
                    complexity=self._calc_complexity(node),
                    lines=self._get_lines(node)
                ))
        return functions
    
    def _extract_classes(self, tree) -> List[Dict]:
        """Extract all classes"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append({
                    'name': node.name,
                    'line': node.lineno,
                    'methods': methods,
                    'method_count': len(methods)
                })
        return classes
    
    def _extract_imports(self, tree) -> Dict:
        """Extract imports"""
        imports = {'modules': [], 'from_imports': []}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports['modules'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports['from_imports'].append(node.module)
        return imports
    
    def _calculate_metrics(self, code: str, tree) -> CodeMetrics:
        """Calculate code metrics"""
        lines = code.split('\n')
        total_lines = len(lines)
        code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))
        
        functions_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
        classes_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
        complexity = sum(self._calc_complexity(n) for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
        
        return CodeMetrics(
            total_lines=total_lines,
            code_lines=code_lines,
            functions_count=functions_count,
            classes_count=classes_count,
            complexity_score=complexity
        )
    
    def _calc_complexity(self, node) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        return complexity
    
    def _get_lines(self, node) -> int:
        """Get number of lines in node"""
        if hasattr(node, 'end_lineno'):
            return node.end_lineno - node.lineno + 1
        return 0
    
    def _generate_suggestions(self, functions: List[FunctionInfo], classes: List[Dict], code: str) -> List[Dict]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if functions:
            undoc = sum(1 for f in functions if not f.docstring)
            if undoc > 0:
                suggestions.append({
                    'type': 'documentation',
                    'priority': 'high',
                    'title': 'Add Documentation',
                    'message': f'{undoc} function(s) missing docstrings',
                    'action': 'Add docstrings to describe what each function does'
                })
        
        if functions:
            complex_funcs = [f for f in functions if f.complexity > 10]
            if complex_funcs:
                suggestions.append({
                    'type': 'complexity',
                    'priority': 'high',
                    'title': 'Reduce Complexity',
                    'message': f'{len(complex_funcs)} function(s) are too complex',
                    'action': 'Break complex functions into smaller, simpler ones'
                })
        
        if functions:
            long_funcs = [f for f in functions if f.lines > 50]
            if long_funcs:
                suggestions.append({
                    'type': 'maintainability',
                    'priority': 'medium',
                    'title': 'Shorten Functions',
                    'message': f'{len(long_funcs)} function(s) are too long',
                    'action': 'Keep functions under 50 lines for better readability'
                })
        
        return suggestions
    
    def _detect_skill_gaps(self, code: str, functions: List[FunctionInfo], classes: List[Dict]) -> List[Dict]:
        """Detect missing programming skills"""
        gaps = []
        
        if 'try:' not in code and 'except' not in code and len(functions) > 2:
            gaps.append({
                'skill': 'Error Handling',
                'reason': 'No try-except blocks detected',
                'importance': 'high',
                'learn_time': '2 hours'
            })
        
        if not classes and len(functions) > 5:
            gaps.append({
                'skill': 'Object-Oriented Programming',
                'reason': 'Code uses only functions, no classes',
                'importance': 'high',
                'learn_time': '4 hours'
            })
        
        if functions:
            doc_count = sum(1 for f in functions if f.docstring)
            if doc_count == 0:
                gaps.append({
                    'skill': 'Code Documentation',
                    'reason': 'No docstrings found in any function',
                    'importance': 'medium',
                    'learn_time': '1 hour'
                })
        
        if 'def ' in code and '->' not in code:
            gaps.append({
                'skill': 'Type Hints',
                'reason': 'No type annotations detected',
                'importance': 'medium',
                'learn_time': '1.5 hours'
            })
        
        if ('requests.' in code or 'urllib' in code) and 'async' not in code:
            gaps.append({
                'skill': 'Async Programming',
                'reason': 'Using synchronous I/O operations',
                'importance': 'medium',
                'learn_time': '3 hours'
            })
        
        return gaps