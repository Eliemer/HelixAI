from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
    'pytorch',
    'pandas',
]

setup(
    name='capstone',
    version='0.0',
    description='Capstone project 2020',
    author='Eliemer E. Velez, Luis M. Cintron, Jonathan A. Irizarry',
    author_email='eliemer.velez@upr.edu',
    keywords='web flask deep-learning pytorch',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires 
)
