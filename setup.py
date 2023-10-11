from setuptools import find_packages, setup

from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:

    with open(file_path) as file:
        requirements = file.readlines()
    
    return [require.strip() for require in requirements if not HYPEN_E_DOT in require]


    
setup(
    name='Simple Machine Learing',
    version='0.1.0',
    description='This is a simple machine learing project.',
    author='Ganesh',
    author_email='gs000@pm.me',
    license='GNU',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()
)
