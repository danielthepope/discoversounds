from setuptools import find_packages, setup

setup(
    name='discoversounds',
    version='0.1.0',
    url='https://github.com/danielthepope/discoversounds',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'unidecode'
    ],
    license='MIT'
)
