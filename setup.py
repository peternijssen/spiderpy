from setuptools import setup, find_packages

setup(name='itho_daalderop_api',
      version='1.0.0',
      description='Python wrapper for the Itho Daalderop API, a way to manage your Spider installation',
      url='https://www.github.com/ptnijssen/python-itho-daalderop-api/',
      author='Peter Nijssen',
      author_email='peter@peternijssen.nl',
      license='MIT',
      install_requires=['requests>=2.0'],
      packages=find_packages(),
      zip_safe=True)