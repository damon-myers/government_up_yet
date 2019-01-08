from setuptools import setup

setup(
    name='government-up-yet',
    entry_points={
        'console_scripts': [
            'government_up_yet=app_factory:cli'
        ]
    }
)
