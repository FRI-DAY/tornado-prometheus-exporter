from setuptools import find_packages, setup

setup(
    name='tornado-prometheus-exporter',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/FRI-DAY/tornado-prometheus-exporter',
    license='MIT',
    install_requires=['tornado', 'prometheus-client'],
    author='Sebastian Brandt',
    author_email='sebastian.brandt@friday.de',
    description='Prometheus exporter for Tornado applications',
)
