from setuptools import setup

setup(name='human_feedback_api',
    version='0.0.1',
    install_requires=[
        'Django==1.8',
        'dj_database_url',
        'gunicorn',
        'whitenoise==3',
        'ipython',
    ]
)
