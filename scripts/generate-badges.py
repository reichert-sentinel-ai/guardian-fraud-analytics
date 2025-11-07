"""
Generate shields.io badge markdown for Guardian project.

Enhanced with:
- Model performance badges (from metrics.json)
- Dataset information badges
- Better organization and formatting
- Dynamic badge generation
"""

import json
from pathlib import Path


def generate_shields_badges():
    """Generate shields.io badge markdown for tech stack"""
    
    tech_stack = {
        'Python': {'version': '3.11+', 'color': 'blue', 'logo': 'python'},
        'FastAPI': {'version': '0.104+', 'color': '009688', 'logo': 'fastapi'},
        'React': {'version': '18+', 'color': '61DAFB', 'logo': 'react'},
        'PostgreSQL': {'version': '15+', 'color': '4169E1', 'logo': 'postgresql'},
        'Neo4j': {'version': '5.0+', 'color': '008CC1', 'logo': 'neo4j'},
        'Docker': {'version': '', 'color': '2496ED', 'logo': 'docker'},
        'Redis': {'version': '7.0+', 'color': 'DC382D', 'logo': 'redis'},
        'XGBoost': {'version': '2.0+', 'color': 'red', 'logo': 'xgboost'},
        'scikit-learn': {'version': '1.3+', 'color': 'F7931E', 'logo': 'scikit-learn'},
        'TypeScript': {'version': '5.0+', 'color': '3178C6', 'logo': 'typescript'},
        'Tailwind CSS': {'version': '3.3+', 'color': '38B2AC', 'logo': 'tailwind-css'},
    }
    
    badges = []
    for tech, details in tech_stack.items():
        version_text = details['version'] if details['version'] else ''
        # Handle tech names with spaces (e.g., "Tailwind CSS")
        tech_url = tech.replace(' ', '%20').replace('-', '--')  # shields.io uses -- for hyphens
        badge = f"![{tech}](https://img.shields.io/badge/{tech_url}-{version_text}-{details['color']}?logo={details['logo']}&logoColor=white)"
        badges.append(badge)
    
    return '\n'.join(badges)


def generate_status_badges():
    """Generate project status badges"""
    
    status_badges = [
        "![License](https://img.shields.io/badge/license-MIT-green)",
        "![Status](https://img.shields.io/badge/status-demonstration-yellow)",
        "![Portfolio](https://img.shields.io/badge/type-portfolio%20project-orange)",
    ]
    
    return '\n'.join(status_badges)


def generate_category_badges():
    """Generate category badges for ML, Graph, Deployment"""
    
    category_badges = [
        "![ML](https://img.shields.io/badge/ML-XGBoost%20%7C%20scikit--learn-red)",
        "![Graph](https://img.shields.io/badge/Graph-NetworkX%20%7C%20Neo4j-purple)",
        "![Deployment](https://img.shields.io/badge/deployment-Docker%20%7C%20AWS-orange)",
    ]
    
    return '\n'.join(category_badges)


def generate_model_performance_badges(metrics_path: Path = None):
    """Generate model performance badges from metrics.json"""
    
    if metrics_path is None:
        # Try to find metrics.json relative to script location
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        metrics_path = project_root / "reports" / "metrics.json"
    
    badges = []
    
    if metrics_path.exists():
        try:
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            
            # Format metrics with 2 decimal places
            if 'accuracy' in metrics:
                acc = metrics['accuracy']
                color = 'brightgreen' if acc >= 0.95 else 'green' if acc >= 0.90 else 'yellow'
                badges.append(f"![Accuracy](https://img.shields.io/badge/accuracy-{acc*100:.1f}%-{color})")
            
            if 'auc_roc' in metrics:
                auc = metrics['auc_roc']
                color = 'brightgreen' if auc >= 0.95 else 'green' if auc >= 0.90 else 'yellow'
                badges.append(f"![AUC-ROC](https://img.shields.io/badge/AUC--ROC-{auc:.3f}-{color})")
            
            if 'f1_score' in metrics:
                f1 = metrics['f1_score']
                color = 'brightgreen' if f1 >= 0.90 else 'green' if f1 >= 0.80 else 'yellow'
                badges.append(f"![F1 Score](https://img.shields.io/badge/F1-{f1:.3f}-{color})")
            
            if 'precision' in metrics:
                prec = metrics['precision']
                color = 'brightgreen' if prec >= 0.90 else 'green' if prec >= 0.80 else 'yellow'
                badges.append(f"![Precision](https://img.shields.io/badge/precision-{prec:.3f}-{color})")
            
            if 'recall' in metrics:
                rec = metrics['recall']
                color = 'brightgreen' if rec >= 0.90 else 'green' if rec >= 0.80 else 'yellow'
                badges.append(f"![Recall](https://img.shields.io/badge/recall-{rec:.3f}-{color})")
            
        except Exception as e:
            # If metrics file exists but can't be read, return empty
            pass
    
    # If no metrics found, add placeholder
    if not badges:
        badges = [
            "![Model](https://img.shields.io/badge/model-trained-blue)",
            "![Training](https://img.shields.io/badge/training-fast%20iteration-orange)"
        ]
    
    return '\n'.join(badges)


def generate_dataset_badges():
    """Generate dataset information badges"""
    
    dataset_badges = [
        "![Dataset](https://img.shields.io/badge/dataset-synthetic%20(100K)-blue)",
        "![Training Time](https://img.shields.io/badge/training~5-15%20min-orange)",
        "![Data Type](https://img.shields.io/badge/type-fraud%20detection-red)",
    ]
    
    return '\n'.join(dataset_badges)


def generate_quick_start_badges():
    """Generate quick start/demo badges"""
    
    quick_start_badges = [
        "![Quick Demo](https://img.shields.io/badge/demo-ready-success)",
        "![Fast Iteration](https://img.shields.io/badge/iteration-fast-brightgreen)",
    ]
    
    return '\n'.join(quick_start_badges)


def main():
    """Main function to generate all badge sections"""
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print("# Professional Badges for README.md")
    print("\nCopy the sections below into your README.md:\n")
    
    print("## Top Row - Tech Stack & Status")
    print("\n" + generate_shields_badges())
    print("\n" + generate_status_badges())
    
    print("\n\n## Model Performance")
    metrics_path = project_root / "reports" / "metrics.json"
    print("\n" + generate_model_performance_badges(metrics_path))
    
    print("\n\n## Dataset Information")
    print("\n" + generate_dataset_badges())
    
    print("\n\n## Category Badges")
    print("\n" + generate_category_badges())
    
    print("\n\n## Quick Start Badges")
    print("\n" + generate_quick_start_badges())
    
    print("\n\n---")
    print("\n**Note:** Model performance badges are auto-generated from `reports/metrics.json`.")
    print("Run `python scripts/train_quick_model.py` to generate metrics.")


if __name__ == "__main__":
    main()
