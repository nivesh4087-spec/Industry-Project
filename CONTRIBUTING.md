# Contributing Guidelines

All contributions — bug reports, bug fixes, documentation improvements, enhancements, and ideas — are welcome!

---

## 📋 Table of Contents

- [Development Setup](#-development-setup)
- [Project Conventions](#-project-conventions)
- [Code Style](#-code-style)
- [Running Tests](#-running-tests)
- [How to Contribute](#-how-to-contribute)
- [Pull Request Guidelines](#-pull-request-guidelines)

---

## 🛠️ Development Setup

```bash
# Clone and enter the repo
git clone <repository-url>
cd Manufacturing_Failure_Prevention-

# Create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### First-time training (required for dashboard)

```bash
python scripts/train_pipeline.py
streamlit run app/main.py
```

---

## 📐 Project Conventions

### Config-Driven Design

**All tunable parameters belong in `config/config.yaml`** — not hardcoded in source files.
This includes model hyperparameters, thresholds, file paths, feature names, business cost values, and risk scoring parameters.

```python
# ✅ Good — read from config
threshold = config["risk"]["thresholds"]["high"]

# ❌ Bad — hardcoded magic number
threshold = 80
```

### Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `src/data/` | Loading, downloading, validating raw data |
| `src/preprocessing/` | Cleaning, encoding, scaling (fit on train only!) |
| `src/features/` | Physics-informed feature engineering |
| `src/models/` | Training, HPO, calibration, artifact management |
| `src/evaluation/` | Metrics computation and plot generation |
| `src/explainability/` | SHAP global and local explanations |
| `src/risk/` | Risk scoring and early warning |
| `src/recommendations/` | Rule-based maintenance recommendations |
| `app/` | Streamlit dashboard only — no ML logic here |

### No Data Leakage

**Critical rule:** All `fit()` operations (scalers, statistics, thresholds) must use **training data only**.
Pass pre-computed stats to validation/test transforms. This is enforced throughout the codebase — please maintain it.

---

## 🎨 Code Style

- Follow **PEP 8** — use a formatter like `black` or `autopep8`
- Use **type hints** on all function signatures
- Write **Google-style docstrings** for all functions and classes:

```python
def compute_risk_score(failure_probability: float, config: dict) -> float:
    """Transform failure probability into a 0-100 risk score.

    Args:
        failure_probability: Calibrated failure probability (0-1).
        config: Project configuration dictionary.

    Returns:
        Risk score in [0, 100].
    """
```

- Use `logger = logging.getLogger(__name__)` in every module — no bare `print()` statements in library code
- Keep functions focused and short — prefer composing small functions over large monolithic ones

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/test_features.py -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=term-missing
```

Tests live in `tests/` and mirror the `src/` structure. When adding a new feature, add corresponding tests.

---

## 🤝 How to Contribute

1. **Fork** the repository
2. **Create a branch** for your change:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
3. **Make your changes** following the code style guidelines above
4. **Run tests** to confirm nothing is broken:
   ```bash
   python -m pytest tests/ -v
   ```
5. **Commit** with a clear message:
   ```bash
   git commit -m "feat: add SMOTE comparison to ablation study"
   # or
   git commit -m "fix: remove duplicate temp_diff assignment in engineer.py"
   ```
6. **Push** your branch and open a **Pull Request**

---

## 📝 Pull Request Guidelines

- Keep PRs focused — one logical change per PR
- Reference any related issues in the PR description
- Describe **what** changed and **why**, not just how
- Include test coverage for new functionality
- Update `README.md` or docstrings if the change affects public-facing behaviour

---

## 🚫 What Not to Commit

See `.gitignore` — but the key items are:

- Model artifacts (`models/*.joblib`, etc.) — these are generated, not source
- Dataset files (`*.csv`, `*.zip`) — too large; the pipeline downloads automatically
- Generated reports (`reports/figures/`, `reports/results/`)
- Assignment / submission documents (`*.docx`, `*.pdf`)
- Virtual environments (`venv/`, `.venv/`)
