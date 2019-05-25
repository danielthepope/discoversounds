from setuptools import find_packages, setup

setup(
    name='discoversounds',
    version='0.1.0',
    url='https://github.com/danielthepope/discoversounds',
    packages=find_packages(),
    install_requires=[
        'Flask==1.0.2',
        'Flask-RESTful==0.3.7',
        'python-dotenv==0.10.1',
        'SQLAlchemy==1.3.2',
        'Unidecode==1.0.23'
    ],
    extras_require={
        'dev': [
            'pylint==1.9.4',
            'rope==0.12.0'
        ],
        'prod': [
            'gunicorn==19.9.0'
        ],
        'test': [
            'pytest==4.5.0'
        ]
    },
    license='MIT'
)
