#!/bin/bash
# Chat 1 Setup Script (Linux/Mac)
# Automates installation of dependencies and configuration

echo "================================================"
echo "Chat 1: Guardian Data Acquisition - Setup"
echo "================================================"
echo ""

# Step 1: Check Python version
echo "[1/4] Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION"
    
    # Extract version number
    if [[ $PYTHON_VERSION =~ Python[[:space:]]+([0-9]+)\.([0-9]+) ]]; then
        MAJOR=${BASH_REMATCH[1]}
        MINOR=${BASH_REMATCH[2]}
        
        if [[ $MAJOR -lt 3 ]] || [[ $MAJOR -eq 3 && $MINOR -lt 11 ]]; then
            echo "⚠ Warning: Python 3.11+ recommended"
        fi
    fi
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✓ $PYTHON_VERSION"
    PYTHON_CMD=python
else
    echo "✗ Python not found. Please install Python 3.11+"
    exit 1
fi
echo ""

# Step 2: Install dependencies
echo "[2/4] Installing dependencies..."
echo "This may take a few minutes..."

PACKAGES=(
    "kaggle"
    "pandas"
    "numpy"
    "scikit-learn"
    "xgboost"
    "shap"
    "fastapi"
    "uvicorn"
    "python-dotenv"
)

INSTALLED=0
FAILED=0

for package in "${PACKAGES[@]}"; do
    echo -n "  Installing $package... "
    if $PYTHON_CMD -m pip install -q "$package" 2>/dev/null; then
        INSTALLED=$((INSTALLED + 1))
        echo "✓"
    else
        FAILED=$((FAILED + 1))
        echo "✗"
    fi
done

echo ""
echo "✓ Installed: $INSTALLED/${#PACKAGES[@]} packages"
if [ $FAILED -gt 0 ]; then
    echo "✗ Failed: $FAILED packages"
fi
echo ""

# Step 3: Check Kaggle API configuration
echo "[3/4] Checking Kaggle API configuration..."

KAGGLE_DIR="$HOME/.kaggle"
KAGGLE_JSON="$KAGGLE_DIR/kaggle.json"

if [ -f "$KAGGLE_JSON" ]; then
    echo "✓ Kaggle API credentials found"
    KAGGLE_CONFIGURED=true
else
    echo "✗ Kaggle API credentials NOT found"
    echo ""
    echo "To configure Kaggle API:"
    echo "  1. Go to: https://www.kaggle.com/settings"
    echo "  2. Click 'Create New Token' in the API section"
    echo "  3. Download kaggle.json"
    echo "  4. Place it in: $KAGGLE_JSON"
    echo "  5. Set permissions: chmod 600 $KAGGLE_JSON"
    echo ""
    
    # Offer to create directory
    if [ ! -d "$KAGGLE_DIR" ]; then
        read -p "Create .kaggle directory? (Y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            mkdir -p "$KAGGLE_DIR"
            echo "✓ Directory created: $KAGGLE_DIR"
        fi
    fi
    
    KAGGLE_CONFIGURED=false
fi
echo ""

# Step 4: Verify installations
echo "[4/4] Verifying installations..."

MISSING_MODULES=()

MODULES=("kaggle" "pandas" "numpy" "sklearn" "xgboost")
for module in "${MODULES[@]}"; do
    if $PYTHON_CMD -c "import $module" 2>/dev/null; then
        echo "  ✓ $module"
    else
        echo "  ✗ $module"
        MISSING_MODULES+=("$module")
    fi
done
echo ""

# Summary
echo "================================================"
echo "Setup Summary"
echo "================================================"

ALL_GOOD=true

# Check Python
echo -n "Python: "
if command -v $PYTHON_CMD &> /dev/null; then
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
    echo "✓ $PYTHON_VERSION"
else
    echo "✗ Not found"
    ALL_GOOD=false
fi

# Check dependencies
echo -n "Dependencies: "
if [ ${#MISSING_MODULES[@]} -eq 0 ]; then
    echo "✓ All installed"
else
    echo "✗ Missing: ${MISSING_MODULES[*]}"
    ALL_GOOD=false
fi

# Check Kaggle
echo -n "Kaggle API: "
if [ "$KAGGLE_CONFIGURED" = true ]; then
    echo "✓ Configured"
else
    echo "✗ Not configured"
    ALL_GOOD=false
fi

echo ""

if [ "$ALL_GOOD" = true ]; then
    echo "✓ Setup complete! Ready to run Chat 1."
    echo ""
    echo "Next step:"
    echo "  python scripts/run_chat1.py"
else
    echo "⚠ Setup incomplete. Please address the issues above."
    echo ""
    echo "See RUN_CHAT1_STATUS.md for detailed instructions."
fi

echo ""

