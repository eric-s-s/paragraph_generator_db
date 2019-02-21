from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


VERSION = '0.1'

setup(name='db_interface',
      version=VERSION,
      description='database control for paragraph generator',
      long_description=readme(),
      keywords='',
      url='http://github.com/eric-s-s/db_interface',
      author='Eric Shaw',
      author_email='shaweric01@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False)
