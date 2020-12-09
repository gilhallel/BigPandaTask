from setuptools import setup

setup(
    name='stream_processing_service',
    packages=['stream_processing_service'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)