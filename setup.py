from setuptools import setup


def read_requirements():
    """
    Read a python requirements.txt file.
    """
    with open('requirements.txt') as fh:
        return [
            line.strip()
            for line in fh
            if not line.startswith('#')]

setup(
    name='pyphpbb',
    version='0.0.1',
    author='Justin Fay',
    author_email='mail@justinfay.me',
    packages=['pyphpbb'],
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'pyphpbb = pyphpbb.__main__:main']})
