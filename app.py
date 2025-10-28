import streamlit as st
import sys
sys.path.insert(0, 'src')

from analyzer.code_analyzer import CodeAnalyzer
from analyzer.error_detector import ErrorDetector
from scanner.security_scanner import SecurityScanner
from generator.report_generator import ReportGenerator
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="DevInsight AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0

# CLEAN CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .block-container {
        padding: 2rem;
        max-width: 1400px;
    }
    
    h1 {
        color: #1a1a1a;
        font-weight: 800;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 700;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
    }
    
    p {
        color: #4a5568;
        line-height: 1.6;
    }
    
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    [data-testid="stMetricValue"] {
        color: #1a1a1a;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #718096;
        font-weight: 600;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        color: #4a5568;
        font-weight: 600;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    .stTextArea textarea {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        color: #1a1a1a;
        font-family: 'Monaco', monospace;
        font-size: 14px;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
    }
    
    .stSuccess {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        color: #065f46;
    }
    
    .stInfo {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        color: #1e40af;
    }
    
    .stWarning {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        color: #92400e;
    }
    
    .stError {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        color: #991b1b;
    }
    
    .streamlit-expanderHeader {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        color: #1a1a1a;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white;
    }
    
    .stat-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #e2e8f0;
    }
    
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-high { background: #fee2e2; color: #991b1b; }
    .badge-medium { background: #fef3c7; color: #92400e; }
    .badge-low { background: #d1fae5; color: #065f46; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
    }
    
    a:hover {
        color: #764ba2;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1>🧠 DevInsight AI</h1>
    <p style='font-size: 1.25rem; color: #718096;'>
        Intelligent Code Analysis & Learning Platform
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Dashboard")
    
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;'>
        <h3 style='color: white; margin: 0;'>📊 Session Stats</h3>
        <h1 style='color: white; font-size: 3rem; margin: 0.5rem 0;'>{st.session_state.analysis_count}</h1>
        <p style='color: rgba(255,255,255,0.8); margin: 0;'>Analyses Run</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 💡 Quick Tips")
    st.info("**Best Practices:**\n- Keep functions under 50 lines\n- Add docstrings\n- Use type hints\n- Handle errors properly")
    
    st.markdown("---")
    
    st.markdown("### 📚 Resources")
    st.markdown("""
    - [Python Docs](https://docs.python.org)
    - [Real Python](https://realpython.com)
    - [PEP 8 Guide](https://pep8.org)
    """)

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Analyze", "🐛 Errors", "🔒 Security", "🎓 Learn", "💡 Improve"])

with tab1:
    st.markdown("## 📝 Code Analysis")
    
    input_method = st.radio(
        "Choose input method:",
        ["Paste Code", "Upload File", "GitHub URL"],
        horizontal=True
    )
    
    code_input = None
    
    if input_method == "Paste Code":
        code_input = st.text_area(
            "Enter your Python code:",
            height=300,
            placeholder="# Paste your Python code here...\n\ndef example():\n    pass"
        )
    
    elif input_method == "Upload File":
        uploaded = st.file_uploader("Choose a Python file", type=['py'])
        if uploaded:
            code_input = uploaded.read().decode('utf-8')
            st.success(f"✅ Loaded: {uploaded.name}")
    
    else:
        github_url = st.text_input(
            "GitHub file URL:",
            placeholder="https://github.com/user/repo/blob/main/file.py"
        )
        
        if github_url and st.button("Fetch Code"):
            import requests
            raw_url = github_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
            try:
                response = requests.get(raw_url, timeout=10)
                if response.status_code == 200:
                    code_input = response.text
                    st.success(f"✅ Fetched {len(code_input)} characters")
                else:
                    st.error("Failed to fetch. Try copying code manually.")
            except:
                st.error("Error fetching. Please paste code manually.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Analyze Code", type="primary"):
        if code_input:
            st.session_state.analysis_count += 1
            
            with st.spinner("Analyzing..."):
                # Error detection
                error_detector = ErrorDetector()
                errors = error_detector.detect_all_issues(code_input)
                st.session_state['errors'] = errors
                
                if errors:
                    critical_errors = [e for e in errors if e['severity'] == 'ERROR']
                    warnings = [e for e in errors if e['severity'] == 'WARNING']
                    
                    if critical_errors:
                        st.error(f"🚨 Found {len(critical_errors)} error(s)!")
                        
                        for err in critical_errors[:3]:
                            with st.expander(f"❌ Line {err['line']}: {err['issue']}", expanded=True):
                                st.markdown(f"**Cause:** {err['cause']}")
                                if err['code_snippet']:
                                    st.code(err['code_snippet'], language='python')
                                st.success(f"**Fix:** {err['fix']}")
                    
                    if warnings:
                        st.warning(f"⚠️ {len(warnings)} warning(s) - Check 🐛 Errors tab")
                
                # Normal analysis
                analyzer = CodeAnalyzer()
                results = analyzer.analyze(code_input)
                
                scanner = SecurityScanner()
                security_issues = scanner.scan(code_input)
                security_score = scanner.get_security_score(security_issues)
                
                st.session_state['results'] = results
                st.session_state['code'] = code_input
                st.session_state['security_issues'] = security_issues
                st.session_state['security_score'] = security_score
                
                if results['success']:
                    if not errors:
                        st.success("✅ No errors found!")
                    
                    st.markdown("### 📊 Code Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Lines", results['metrics']['total_lines'])
                    with col2:
                        st.metric("Functions", results['metrics']['functions_count'])
                    with col3:
                        st.metric("Classes", results['metrics']['classes_count'])
                    with col4:
                        st.metric("Complexity", results['metrics']['complexity_score'])
                    
                    if results['functions']:
                        st.markdown("### 📦 Functions")
                        for func in results['functions']:
                            with st.expander(f"**{func['name']}()** - Line {func['line_number']}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Arguments:** {len(func['args'])}")
                                    st.write(f"**Complexity:** {func['complexity']}")
                                with col2:
                                    st.write(f"**Lines:** {func['lines']}")
                                    doc_status = "✅" if func['docstring'] else "❌"
                                    st.write(f"**Documented:** {doc_status}")
                    
                    if results['classes']:
                        st.markdown("### 🏗️ Classes")
                        for cls in results['classes']:
                            st.info(f"**{cls['name']}** - {cls['method_count']} methods")
                else:
                    st.error(f"Error: {results['error']}")
        else:
            st.warning("Please enter some code first")

with tab2:
    st.markdown("## 🐛 Error Detection")
    
    if 'errors' in st.session_state and st.session_state['errors']:
        errors = st.session_state['errors']
        
        total_errors = len([e for e in errors if e['severity'] == 'ERROR'])
        total_warnings = len([e for e in errors if e['severity'] == 'WARNING'])
        total_style = len([e for e in errors if e['severity'] == 'STYLE'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='stat-card' style='border-top: 4px solid #ef4444;'>
                <h1 style='color: #ef4444; margin: 0;'>{total_errors}</h1>
                <p style='color: #718096;'>Errors</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='stat-card' style='border-top: 4px solid #f59e0b;'>
                <h1 style='color: #f59e0b; margin: 0;'>{total_warnings}</h1>
                <p style='color: #718096;'>Warnings</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='stat-card' style='border-top: 4px solid #3b82f6;'>
                <h1 style='color: #3b82f6; margin: 0;'>{total_style}</h1>
                <p style='color: #718096;'>Style Issues</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 All Issues")
        
        for err in errors:
            severity_emoji = {'ERROR': '🔴', 'WARNING': '🟡', 'STYLE': '🔵'}[err['severity']]
            severity_color = {'ERROR': '#fef2f2', 'WARNING': '#fffbeb', 'STYLE': '#eff6ff'}[err['severity']]
            border_color = {'ERROR': '#ef4444', 'WARNING': '#f59e0b', 'STYLE': '#3b82f6'}[err['severity']]
            
            st.markdown(f"""
            <div style='background: {severity_color}; padding: 1.5rem; border-radius: 8px; border-left: 4px solid {border_color}; margin: 1rem 0;'>
                <h4 style='margin: 0 0 0.5rem 0;'>{severity_emoji} Line {err['line']}: {err['issue']}</h4>
                <p style='margin: 0.5rem 0;'><strong>Cause:</strong> {err['cause']}</p>
                <p style='margin: 0.5rem 0;'><strong>Fix:</strong> {err['fix']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if err.get('code_snippet'):
                st.code(err['code_snippet'], language='python')
    
    elif 'errors' in st.session_state and not st.session_state['errors']:
        st.success("🎉 No errors detected! Your code is clean!")
    
    else:
        st.info("👈 Analyze code first to detect errors")

with tab3:
    st.markdown("## 🔒 Security Analysis")
    
    if 'security_score' in st.session_state:
        score = st.session_state['security_score']
        issues = st.session_state['security_issues']
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f"""
            <div class='stat-card'>
                <h1 style='font-size: 4rem; margin: 0; color: {"#10b981" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"};'>{score}</h1>
                <p style='color: #718096; font-size: 1.25rem; margin: 0.5rem 0 0 0;'>Security Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if issues:
            st.warning(f"Found {len(issues)} security issue(s)")
            
            for issue in issues:
                severity_badge = {'HIGH': 'badge-high', 'MEDIUM': 'badge-medium', 'LOW': 'badge-low'}[issue['severity']]
                
                with st.expander(f"Line {issue['line']}: {issue['description']}"):
                    st.markdown(f"<span class='badge {severity_badge}'>{issue['severity']}</span>", unsafe_allow_html=True)
                    st.code(issue['code'], language='python')
                    st.info(f"💡 **Fix:** {issue['recommendation']}")
        else:
            st.success("🎉 No security issues detected!")
    else:
        st.info("👈 Analyze code first")

with tab4:
    st.markdown("## 🎓 Personalized Learning Path")
    
    if 'results' in st.session_state and st.session_state['results'].get('skill_gaps'):
        gaps = st.session_state['results']['skill_gaps']
        
        st.info(f"📚 Found {len(gaps)} skill(s) to learn")
        
        for i, gap in enumerate(gaps, 1):
            with st.expander(f"{i}. {gap['skill']} - {gap['learn_time']}", expanded=(i==1)):
                st.markdown(f"**Why learn this:** {gap['reason']}")
                st.markdown(f"**Priority:** {gap['importance'].upper()}")
                
                st.markdown("### 📚 Learning Resources")
                
                resources = {
                    "Error Handling": {
                        "videos": [
                            ("Python Error Handling", "https://www.youtube.com/watch?v=NIWwJbo-9_8"),
                            ("Exceptions Tutorial", "https://www.youtube.com/watch?v=6SPDvPK38tw")
                        ],
                        "articles": [
                            ("Real Python - Exceptions", "https://realpython.com/python-exceptions/"),
                            ("Python Docs", "https://docs.python.org/3/tutorial/errors.html")
                        ]
                    },
                    "Object-Oriented Programming": {
                        "videos": [
                            ("OOP in Python", "https://www.youtube.com/watch?v=JeznW_7DlB0"),
                            ("Python Classes", "https://www.youtube.com/watch?v=ZDa-Z5JzLYM")
                        ],
                        "articles": [
                            ("Real Python OOP", "https://realpython.com/python3-object-oriented-programming/"),
                            ("W3Schools", "https://www.w3schools.com/python/python_classes.asp")
                        ]
                    },
                    "Type Hints": {
                        "videos": [
                            ("Python Type Hints", "https://www.youtube.com/watch?v=QORvB-_mbZ0"),
                        ],
                        "articles": [
                            ("Real Python Typing", "https://realpython.com/python-type-checking/"),
                        ]
                    },
                    "Code Documentation": {
                        "videos": [
                            ("Python Docstrings", "https://www.youtube.com/watch?v=0YUdYk5E-w4"),
                        ],
                        "articles": [
                            ("PEP 257", "https://peps.python.org/pep-0257/"),
                        ]
                    },
                    "Async Programming": {
                        "videos": [
                            ("Async Python", "https://www.youtube.com/watch?v=t5Bo1Je9EmE"),
                        ],
                        "articles": [
                            ("Real Python Async", "https://realpython.com/async-io-python/"),
                        ]
                    }
                }
                
                skill_resources = resources.get(gap['skill'], {
                    "videos": [("YouTube Search", f"https://www.youtube.com/results?search_query=python+{gap['skill'].replace(' ', '+')}+tutorial")],
                    "articles": [("Real Python", "https://realpython.com")]
                })
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📺 Video Tutorials:**")
                    for title, url in skill_resources.get('videos', []):
                        st.markdown(f"- [{title}]({url})")
                
                with col2:
                    st.markdown("**📝 Articles:**")
                    for title, url in skill_resources.get('articles', []):
                        st.markdown(f"- [{title}]({url})")
    else:
        st.info("👈 Analyze code first")

with tab5:
    st.markdown("## 💡 Improvement Suggestions")
    
    if 'results' in st.session_state and st.session_state['results'].get('suggestions'):
        suggestions = st.session_state['results']['suggestions']
        
        for i, sugg in enumerate(suggestions, 1):
            priority_badge = {'high': 'badge-high', 'medium': 'badge-medium', 'low': 'badge-low'}[sugg['priority']]
            
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #e2e8f0; margin: 1rem 0;'>
                <h4>{i}. {sugg['title']}</h4>
                <p><strong>Issue:</strong> {sugg['message']}</p>
                <p><strong>Action:</strong> {sugg['action']}</p>
                <span class='badge {priority_badge}'>{sugg['priority'].upper()}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👈 Analyze code first")

# Download
if 'results' in st.session_state and st.session_state['results'].get('success'):
    st.markdown("---")
    st.markdown("### 📥 Export Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            report_gen = ReportGenerator()
            markdown_report = report_gen.generate_markdown_report(
                st.session_state['results'],
                st.session_state['code']
            )
            st.download_button(
                "📄 Markdown",
                markdown_report,
                "report.md",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
    
    with col2:
        try:
            import json
            json_export = json.dumps(st.session_state['results'], indent=2)
            st.download_button(
                "📊 JSON",
                json_export,
                "analysis.json",
                use_container_width=True
            )
        except:
            pass
    
    with col3:
        try:
            st.download_button(
                "💾 Code",
                st.session_state['code'],
                "code.py",
                use_container_width=True
            )
        except:
            pass

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; padding: 2rem;'>
    <p><strong>DevInsight AI</strong> - Made with ❤️</p>
    <p>
        <a href='https://github.com/yourusername/devinsight-ai'>GitHub</a> • 
        <a href='https://linkedin.com/in/yourprofile'>LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)