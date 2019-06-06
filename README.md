find-out
==============================

Find Out is an the sister project to the open source project Opt Out. It is here to enable the study different machine learning models and their ability to classify sexual harassment text. The project organization is below.

Project Organization
--------------------

    ├── LICENSE
    ├── Makefile           <- (NOT READY) Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    |   ├── benchmark      <- The gold standard dataset.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- (NOT READY YET) A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── collect
    |   |       └── collect_model_datasetname.py
    |   |   └── preprocess
    |   |       └── preprocess_model_datasetname.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── features_model_datasetname.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model_datasetname.py
    │   │   └── train_model_datasetname.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize_model_datasetname.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

Multiple studies will exist in one repo (to begin with). Standardized naming of files and folders is key to the success of this style of collaboration.

The naming convention is: `action_model_datasetname.py`

For example, if I have written a script that will train a neural net using the dataset called datazet, the naming convention would be:
train_nn_datazet.py

Please follow the example in the repository if you're stuck, to run the tests for the example:

``` 
cd find-out
python -m pytest tests/test_nn_dataturks.py
```

NB. this is not a permanent solution but will enable initial effective collaboration. If you have any thoughts or ideas on how to improve this, just email opt.out.tool@gmail.com
