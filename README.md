# Installation
- Create virtual environment
```
python -m venv .venv
```

- Activate environment
```
.venv\Scripts\Activate.ps1
```

- Install dependencies
```
pip install -r requirements.txt
```

# Register Virtual Environment as Jupyter Kernel
```
python -m ipykernel install --user --name eda-python-project --display-name "EDA Python Project"
```

# Run the Notebook
```
python -m notebook