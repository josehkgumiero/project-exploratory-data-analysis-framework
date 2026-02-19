# Installation

- Create virtual environment
```
python -m venv .venv
```

- Activate environment
```
.venv\Scripts\Activate.ps1
```

- Update the PIP
```
python.exe -m pip install --upgrade pip
```

- Install dependencies
```
pip install -r requirements.txt
```

# Register Virtual Environment as Jupyter Kernel
```
python -m ipykernel install --user --name project-eda-final --display-name "Project EDA Final"
```

# Run the Notebook
```
python -m notebook