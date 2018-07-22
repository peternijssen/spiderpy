from setuptools import setup, find_packages

setup(name='spiderpy',
      version='1.0.5',
      description='Python wrapper for the Spider API, a way to manage your Spider installation',
      url='https://www.github.com/ptnijssen/spiderpy/',
      author='Peter Nijssen',
      author_email='peter@peternijssen.nl',
      license='MIT',
      install_requires=['requests>=2.0'],
      packages=find_packages(),
      zip_safe=True)