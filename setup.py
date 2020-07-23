from setuptools import setup, find_packages

requires = [
    'flask',
    'flask_jwt_extended',
    'flask_cors',
    'PyJWT'
    'click',
    'torch',
    'pytorch_lightning',
    'pandas',
    'scipy',
    'pprint',
    'requests'
]

setup(
    name='helix_ai',
    version='1.0',
    description='Capstone project 2020',
    author='Eliemer E. Velez, Luis M. Cintron',
    author_email='eliemer.velez@upr.edu, luis.cintron16@upr.edu',
    keywords='web protein biology microbiology flask deep-learning pytorch pytorch_lightning',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
