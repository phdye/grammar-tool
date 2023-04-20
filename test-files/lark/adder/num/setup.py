from setuptools import setup, find_packages

setup(
    name='grammar',
    version='0.1.1',
    #url='https://github.com/mypackage.git',
    #author='Author Name',
    #author_email='author@gmail.com',
    #description='Description of my package',
    packages=find_packages(),    
    # install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1'],
    requires=['parameterized'],
    setup_requires=['pytest', 'pytest-runner'],
)
