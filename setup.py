import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='qg-mongo-dashboard',
    version='0.0.1',
    description='Dashboard for monitoring on-going MongoDB queries in pretty format',
    url='https://github.com/quantumgraph/qg-mongo-dashboard',
    author='QuantumGraph',
    author_email='contact@quantumgraph.com',
    license='MIT',
    packages=find_packages(),
    long_description=read('README.md'),
    keywords = ['mongodb', 'connection', 'monitoring', 'ongoing', 'current', 'queries', 'table', 'killop', 'utility'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: System :: Monitoring',
        'License :: Freeware',
        'Programming Language :: Python',
    ],
)
