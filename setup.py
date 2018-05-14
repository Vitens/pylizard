from setuptools import setup

setup(name='pyimod',
      version='0.1',
      description='iMOD files read, edit and write',
      url='https://github.com/VitensTC/pyimod/',
      author='Sjoerd Rijpkema',
      author_email='Sjoerd.Rijpkema@vitens.nl',
      packages=['pyimod'],
      install_requires=['pyshp',\
                        'numpy'],
      zip_safe=False)