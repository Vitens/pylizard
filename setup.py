from setuptools import setup

setup(name='pylizard',
      version='0.1',
      description='Lizard',
      url='https://github.com/VitensTC/pylizard/',
      author='Sjoerd Rijpkema',
      author_email='Sjoerd.Rijpkema@vitens.nl',
      packages=['pylizard'],
      install_requires=['requests',
                        'pandas',
                        'pyproj',
                        'datetime',
                        'numpy',
                        'matplotlib'],
      zip_safe=False)
