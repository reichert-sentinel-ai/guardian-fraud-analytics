"""
Visualization utilities for model evaluation.
Creates confusion matrices, ROC curves, and feature importance plots.
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, confusion_matrix, roc_auc_score
from typing import Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class ModelVisualizer:
    """Create evaluation visualizations."""
    
    def __init__(self, visualizations_dir: str = "visualizations"):
        self.visualizations_dir = Path(visualizations_dir)
        self.visualizations_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        save_path: Optional[str] = None,
        title: str = "Confusion Matrix"
    ) -> Path:
        """
        Plot confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            save_path: Path to save plot
            title: Plot title
            
        Returns:
            Path to saved plot
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Not Fraud', 'Fraud'],
            yticklabels=['Not Fraud', 'Fraud']
        )
        plt.title(title, fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        
        if save_path:
            save_path = Path(save_path)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Confusion matrix saved to {save_path}")
        else:
            save_path = self.visualizations_dir / "confusion_matrix.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Confusion matrix saved to {save_path}")
        
        plt.close()
        
        return save_path
    
    def plot_roc_curve(
        self,
        y_true: np.ndarray,
        y_proba: np.ndarray,
        save_path: Optional[str] = None,
        title: str = "ROC Curve"
    ) -> Path:
        """
        Plot ROC curve.
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            save_path: Path to save plot
            title: Plot title
            
        Returns:
            Path to saved plot
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_proba)
        auc = roc_auc_score(y_true, y_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, linewidth=2, label=f'ROC Curve (AUC = {auc:.4f})')
        plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc="lower right", fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            save_path = Path(save_path)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"ROC curve saved to {save_path}")
        else:
            save_path = self.visualizations_dir / "roc_curve.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"ROC curve saved to {save_path}")
        
        plt.close()
        
        return save_path
    
    def plot_feature_importance(
        self,
        feature_importance: pd.DataFrame,
        top_n: int = 20,
        save_path: Optional[str] = None,
        title: str = "Feature Importance"
    ) -> Path:
        """
        Plot feature importance.
        
        Args:
            feature_importance: DataFrame with 'feature' and 'importance' columns
            top_n: Number of top features to display
            save_path: Path to save plot
            title: Plot title
            
        Returns:
            Path to saved plot
        """
        top_features = feature_importance.head(top_n)
        
        plt.figure(figsize=(10, 8))
        sns.barplot(data=top_features, y='feature', x='importance', palette='viridis')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Importance', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        plt.tight_layout()
        
        if save_path:
            save_path = Path(save_path)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Feature importance saved to {save_path}")
        else:
            save_path = self.visualizations_dir / "feature_importance.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Feature importance saved to {save_path}")
        
        plt.close()
        
        return save_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    # visualizer = ModelVisualizer()
    
    # Load test data
    # y_test = pd.read_csv("data/processed/y_test.csv").squeeze()
    
    # Load predictions (example)
    # y_pred = ...
    # y_proba = ...
    
    # Generate plots
    # visualizer.plot_confusion_matrix(y_test, y_pred)
    # visualizer.plot_roc_curve(y_test, y_proba)

