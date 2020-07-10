from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'torch',
    'pandas',
    'pytorch_lightning',
]

setup(
    name='Capstone 2020',
    version='0.0',
    description='Capstone project 2020',
    author='Eliemer E. Velez, Luis M. Cintron, Jonathan A. Irizarry',
    author_email='eliemer.velez@upr.edu, luis.cintron16@upr.edu, jonathan.irizarry3@upr.edu',
    keywords='web flask deep-learning pytorch',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
