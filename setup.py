from setuptools import setup, find_packages

setup(
    name='lppls-script',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lppls-script = lppls_script.main:main'
        ]
    },
    include_package_data=True,
    package_data={
        'lppls-script': ['run.ipynb'],
    },
    install_requires=[
        'lppls',
        'nbconvert',
        'nbformat',
        'requests'
    ],
)
