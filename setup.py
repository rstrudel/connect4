from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# with open(path.join(here, 'README.org'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='connect4',
    version='0.1.dev0',
    description='Connect4 MCTS AI',
    packages=find_packages(),
)
