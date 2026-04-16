from setuptools import setup, find_packages

setup(
    name="ds20195",
    version="0.0.1",
    url="https://github.com/ds20195/notebooks",
    packages=find_packages(),
    install_requires=[
        "census >= 0.8.19",
        "us >= 2.0.2",
        "pandas >= 2.2.2",
        "gspread_pandas >= 3.3.0",
        "tqdm >= 4.0.0",
    ],
)
