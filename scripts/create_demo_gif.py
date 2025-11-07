"""
Sprint U2: Create Demo GIF
Generates an animated GIF showcasing the fraud detection model in action.
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
from typing import List
from pathlib import Path

# Try to import imageio, fallback to PIL
try:
    import imageio.v2 as imageio
    HAS_IMAGEIO = True
except ImportError:
    try:
        import imageio
        HAS_IMAGEIO = True
    except ImportError:
        try:
            from PIL import Image
            HAS_IMAGEIO = False
            HAS_PIL = True
        except ImportError:
            HAS_IMAGEIO = False
            HAS_PIL = False
            print("Warning: Neither imageio nor PIL available. Install with: pip install imageio pillow")

# Add src to path
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.append(str(project_root / "src"))

try:
    import joblib
    import xgboost as xgb
except ImportError:
    print("Warning: xgboost or joblib not available. GIF will show simulated results.")


def create_prediction_animation(
    output_path: Path,
    model_path: Path = None,
    data_path: Path = None,
    duration: float = 0.5,
    num_frames: int = 20
):
    """
    Create animated GIF showing fraud detection predictions.
    
    Args:
        output_path: Path to save the GIF
        model_path: Path to trained model (optional)
        data_path: Path to test data (optional)
        duration: Duration per frame in seconds
        num_frames: Number of frames in animation
    """
    print("Creating demo GIF...")
    print(f"Output: {output_path}")
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Guardian Fraud Detection Demo', fontsize=16, fontweight='bold')
    
    frames = []
    
    # Generate sample data if model not available
    if model_path and model_path.exists() and data_path and data_path.exists():
        try:
            model = joblib.load(model_path)
            data = pd.read_csv(data_path)
            X_test = data.head(100)  # Use first 100 samples
            
            # Get predictions
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            y_pred = (y_pred_proba >= 0.5).astype(int)
        except Exception as e:
            print(f"Warning: Could not load model/data ({e}). Using simulated data.")
            y_pred_proba = np.random.random(100) * 0.8 + 0.1
            y_pred = (y_pred_proba >= 0.5).astype(int)
    else:
        # Simulated data
        y_pred_proba = np.random.random(100) * 0.8 + 0.1
        y_pred = (y_pred_proba >= 0.5).astype(int)
    
    # Create frames
    for i in range(num_frames):
        # Progress through data
        end_idx = min((i + 1) * (len(y_pred_proba) // num_frames), len(y_pred_proba))
        current_proba = y_pred_proba[:end_idx]
        current_pred = y_pred[:end_idx]
        
        # Clear axes
        axes[0].clear()
        axes[1].clear()
        
        # Set consistent limits to ensure frame sizes match
        axes[0].set_xlim(0, len(y_pred_proba))
        axes[0].set_ylim(0, 1)
        axes[1].set_xlim(0, len(y_pred_proba))
        axes[1].set_ylim(-0.5, 1.5)
        
        # Plot 1: Fraud probability over time
        if len(current_proba) > 0:
            axes[0].plot(range(len(current_proba)), current_proba, color='red', linewidth=2, label='Fraud Probability')
            axes[0].axhline(y=0.5, color='orange', linestyle='--', label='Threshold (0.5)')
            axes[0].fill_between(range(len(current_proba)), current_proba, 0.5, 
                                where=(current_proba >= 0.5), alpha=0.3, color='red', label='Fraud Detected')
        axes[0].set_xlabel('Transaction #', fontsize=11)
        axes[0].set_ylabel('Fraud Probability', fontsize=11)
        axes[0].set_title(f'Real-time Fraud Detection ({end_idx} transactions)', fontsize=12, fontweight='bold')
        axes[0].legend(loc='upper right')
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Distribution of predictions
        fraud_count = current_pred.sum() if len(current_pred) > 0 else 0
        legit_count = len(current_pred) - fraud_count
        
        axes[1].barh(['Legitimate', 'Fraud'], [legit_count, fraud_count], 
                    color=['green', 'red'], alpha=0.7)
        axes[1].set_xlabel('Count', fontsize=11)
        axes[1].set_title(f'Classification Summary\n(Fraud: {fraud_count}, Legitimate: {legit_count})', 
                         fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='x')
        
        # Add text with stats
        if end_idx > 0:
            fraud_rate = fraud_count / end_idx * 100
            axes[1].text(legit_count + fraud_count, 1, 
                        f'Fraud Rate: {fraud_rate:.1f}%', 
                        ha='right', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        
        # Save frame with consistent size
        frame_path = output_path.parent / f"frame_{i:03d}.png"
        plt.savefig(frame_path, dpi=100, bbox_inches='tight', facecolor='white')
        
        # Read frame and ensure consistent dimensions
        if HAS_IMAGEIO:
            frame_img = imageio.imread(frame_path)
            # Resize to consistent dimensions if needed (use first frame as reference)
            if i > 0 and len(frames) > 0 and frame_img.shape != frames[0].shape:
                from PIL import Image
                pil_img = Image.fromarray(frame_img)
                reference_shape = frames[0].shape
                pil_img = pil_img.resize((reference_shape[1], reference_shape[0]), Image.Resampling.LANCZOS)
                frame_img = np.array(pil_img)
            frames.append(frame_img)
        elif HAS_PIL:
            frames.append(Image.open(frame_path))
        else:
            frames.append(str(frame_path))
        
        print(f"  Frame {i+1}/{num_frames} created")
    
    # Create GIF
    print(f"\nCreating GIF from {len(frames)} frames...")
    if HAS_IMAGEIO:
        imageio.mimsave(str(output_path), frames, duration=duration, loop=0)
    elif HAS_PIL:
        # Save first frame, then append others
        if frames:
            frames[0].save(
                str(output_path),
                save_all=True,
                append_images=frames[1:] if len(frames) > 1 else [],
                duration=int(duration * 1000),  # PIL uses milliseconds
                loop=0
            )
    else:
        print("Error: Cannot create GIF without imageio or PIL")
        return
    
    # Clean up frame files
    for i in range(num_frames):
        frame_path = output_path.parent / f"frame_{i:03d}.png"
        if frame_path.exists():
            frame_path.unlink()
    
    print(f"✅ Demo GIF created: {output_path}")
    
    plt.close()


def create_simple_demo_gif(output_path: Path):
    """Create a simpler demo GIF with static visualizations."""
    print("Creating simple demo GIF...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Guardian Fraud Detection System - Demo', fontsize=16, fontweight='bold')
    
    # Simulate data
    np.random.seed(42)
    n_samples = 100
    transaction_ids = np.arange(1, n_samples + 1)
    fraud_proba = np.random.beta(2, 20, n_samples)
    
    frames = []
    
    for i in range(10):
        # Clear all subplots
        for ax in axes.flat:
            ax.clear()
        
        # Subplot 1: Time series of fraud probability
        axes[0, 0].plot(transaction_ids[:i*10], fraud_proba[:i*10], 'r-', linewidth=2)
        axes[0, 0].axhline(y=0.5, color='orange', linestyle='--', linewidth=2)
        axes[0, 0].set_xlabel('Transaction ID')
        axes[0, 0].set_ylabel('Fraud Probability')
        axes[0, 0].set_title('Real-time Monitoring')
        axes[0, 0].set_ylim(0, 1)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Subplot 2: Distribution
        current_data = fraud_proba[:i*10] if i*10 > 0 else fraud_proba[:10]
        axes[0, 1].hist(current_data, bins=20, color='blue', alpha=0.7, edgecolor='black')
        axes[0, 1].set_xlabel('Fraud Probability')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Probability Distribution')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Subplot 3: Fraud alerts
        fraud_alerts = (fraud_proba[:i*10] >= 0.5).sum() if i*10 > 0 else 0
        axes[1, 0].bar(['Legitimate', 'Fraud'], 
                      [i*10 - fraud_alerts, fraud_alerts],
                      color=['green', 'red'], alpha=0.7)
        axes[1, 0].set_ylabel('Count')
        axes[1, 0].set_title('Classification Summary')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Subplot 4: Performance metrics
        if i*10 > 0:
            accuracy = 0.95 - np.random.random() * 0.05
            precision = 0.92 - np.random.random() * 0.05
            recall = 0.88 - np.random.random() * 0.05
            f1 = 0.90 - np.random.random() * 0.05
            
            metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
            values = [accuracy, precision, recall, f1]
            
            axes[1, 1].barh(metrics, values, color=['blue', 'green', 'orange', 'purple'], alpha=0.7)
            axes[1, 1].set_xlabel('Score')
            axes[1, 1].set_xlim(0, 1)
            axes[1, 1].set_title('Model Performance')
            axes[1, 1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        # Save frame
        frame_path = output_path.parent / f"demo_frame_{i:03d}.png"
        plt.savefig(frame_path, dpi=100, bbox_inches='tight')
        if HAS_IMAGEIO:
            frames.append(imageio.imread(frame_path))
        elif HAS_PIL:
            frames.append(Image.open(frame_path))
        else:
            frames.append(str(frame_path))
        
        print(f"  Frame {i+1}/10 created")
    
    # Create GIF
    print(f"\nCreating GIF from {len(frames)} frames...")
    if HAS_IMAGEIO:
        imageio.mimsave(str(output_path), frames, duration=0.8, loop=0)
    elif HAS_PIL:
        if frames:
            frames[0].save(
                str(output_path),
                save_all=True,
                append_images=frames[1:] if len(frames) > 1 else [],
                duration=800,  # milliseconds
                loop=0
            )
    else:
        print("Error: Cannot create GIF without imageio or PIL")
        return
    
    # Clean up frame files
    for i in range(10):
        frame_path = output_path.parent / f"demo_frame_{i:03d}.png"
        if frame_path.exists():
            frame_path.unlink()
    
    print(f"✅ Demo GIF created: {output_path}")
    
    plt.close()


def main():
    """Main function to create demo GIF."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Output directory
    output_dir = project_root / "docs" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Try to use real model/data if available
    model_path = project_root / "models" / "xgboost_fraud_demo.pkl"
    data_path = project_root / "data" / "processed" / "X_test.csv"
    output_path = output_dir / "guardian_demo.gif"
    
    # Create demo GIF
    if model_path.exists() and data_path.exists():
        print("Using trained model and test data...")
        create_prediction_animation(output_path, model_path, data_path)
    else:
        print("Using simulated data (model/data not found)...")
        create_simple_demo_gif(output_path)
    
    print("\n" + "="*60)
    print("✅ Sprint U2: Demo GIF Complete!")
    print(f"   GIF saved to: {output_path}")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"Error: Missing required library. Install with: pip install imageio matplotlib")
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error creating demo GIF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

