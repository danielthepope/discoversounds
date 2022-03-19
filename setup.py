from setuptools import find_packages, setup

setup(
    name='discoversounds',
    version='0.2.0',
    url='https://github.com/danielthepope/discoversounds',
    packages=find_packages(),
    install_requires=[
        'aniso8601==9.0.1',
        'click==7.1.2',
        'Flask==1.0.2',
        'Flask-RESTful==0.3.7',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.3',
        'MarkupSafe==1.1.1',
        'python-dotenv==0.10.1',
        'pytz==2021.1',
        'six==1.16.0',
        'SQLAlchemy==1.3.2',
        'Unidecode==1.0.23',
        'Werkzeug==1.0.1',
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
            'pyquery==1.4.0',
            'pytest==4.5.0'
        ]
    },
    license='MIT'
)
