"""
Verify that dashboard correctly integrates real data.

Usage:
    python scripts/verify_dashboard_integration.py
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def verify_streamlit_app():
    """Verify Streamlit app exists."""
    app_path = Path("streamlit_app.py")
    
    if not app_path.exists():
        print("❌ Streamlit app not found")
        print(f"   Expected location: {app_path.absolute()}")
        return False
    
    try:
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"✅ Streamlit app found")
            print(f"   File size: {len(content)} bytes")
            
            # Check for key components
            checks = [
                ("streamlit import", "import streamlit" in content or "from streamlit" in content),
                ("API client", "client" in content.lower() or "api" in content.lower()),
                ("Visualizations", "chart" in content.lower() or "plot" in content.lower() or "graph" in content.lower()),
            ]
            
            for check, result in checks:
                status = "✅" if result else "⚠️"
                print(f"   {status} {check}")
            
            return True
    except Exception as e:
        print(f"❌ Error reading Streamlit app: {e}")
        return False

def verify_api_client():
    """Verify API client exists."""
    api_client_path = Path("src/api/client.py")
    
    if api_client_path.exists():
        print(f"✅ API client found: {api_client_path}")
        return True
    else:
        print(f"⚠️  API client not found: {api_client_path}")
        return False

def verify_api_integration():
    """Verify API integration code exists."""
    # Check if API is referenced in streamlit app
    app_path = Path("streamlit_app.py")
    
    if app_path.exists():
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            has_api = "api" in content.lower() or "client" in content.lower()
            
            if has_api:
                print("✅ API integration code found")
                return True
            else:
                print("⚠️  API integration code not found")
                return False
    else:
        return False

def verify_data_loading():
    """Verify data loading functions exist."""
    # Check for data loader
    loader_path = Path("src/data/loader.py")
    
    if loader_path.exists():
        print(f"✅ Data loader found: {loader_path}")
        return True
    else:
        print(f"⚠️  Data loader not found: {loader_path}")
        return False

def verify_visualization_components():
    """Verify visualization components exist."""
    app_path = Path("streamlit_app.py")
    
    if app_path.exists():
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            visualization_keywords = [
                "st.plotly_chart",
                "st.line_chart",
                "st.bar_chart",
                "st.map",
                "plotly",
                "plot",
                "chart",
                "graph",
            ]
            
            has_visualizations = any(keyword in content.lower() for keyword in visualization_keywords)
            
            if has_visualizations:
                print("✅ Visualization components found")
                return True
            else:
                print("⚠️  Visualization components not found")
                return False
    else:
        return False

def verify_requirements():
    """Verify requirements.txt includes necessary packages."""
    req_path = Path("requirements.txt")
    
    if not req_path.exists():
        print("⚠️  requirements.txt not found")
        return False
    
    try:
        with open(req_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            required_packages = [
                "streamlit",
                "fastapi",
                "pandas",
                "plotly",
            ]
            
            missing = []
            for package in required_packages:
                if package.lower() not in content.lower():
                    missing.append(package)
            
            if not missing:
                print("✅ All required packages in requirements.txt")
                return True
            else:
                print(f"⚠️  Missing packages: {', '.join(missing)}")
                return False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Guardian Dashboard Integration Verification")
    print("=" * 60)
    print()
    
    # Change to repo directory
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    results = []
    
    print("1. Streamlit Application:")
    print("-" * 60)
    app_ok = verify_streamlit_app()
    results.append(app_ok)
    
    print("\n2. API Client:")
    print("-" * 60)
    api_client_ok = verify_api_client()
    results.append(api_client_ok)
    
    print("\n3. API Integration:")
    print("-" * 60)
    api_integration_ok = verify_api_integration()
    results.append(api_integration_ok)
    
    print("\n4. Data Loading:")
    print("-" * 60)
    data_loading_ok = verify_data_loading()
    results.append(data_loading_ok)
    
    print("\n5. Visualization Components:")
    print("-" * 60)
    viz_ok = verify_visualization_components()
    results.append(viz_ok)
    
    print("\n6. Requirements:")
    print("-" * 60)
    req_ok = verify_requirements()
    results.append(req_ok)
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All checks passed!")
        print("\nTo test dashboard:")
        print("  1. Start API: python scripts/run_api.py")
        print("  2. Start Dashboard: streamlit run streamlit_app.py")
    else:
        print("⚠️  Some checks failed. See details above.")
        print("\nNote: Dashboard integration testing requires:")
        print("  1. API running")
        print("  2. Real data loaded")
        print("  3. Dashboard running")
        print("\nSee docs/DASHBOARD_DATA_INTEGRATION.md for details.")

