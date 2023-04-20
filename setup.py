import re

from setuptools import setup, find_packages

package_name = 'grammar_tool'

__version__ = re.search("^__version__\s*=\s*'(.*)'",
                     open(f'{package_name}/__init__.py').read(),
                     re.M ).group(1)

setup(
    name = package_name,
    version = __version__,
    description=r"Grammar Composition and Testing Tool",
    author='Philip H. Dye',
    author_email='philip@phd-solutions.com',
    packages=find_packages(exclude=("s",)),
    requires=['intent_wrap'],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points='''
        [console_scripts]
            grammar-tool = grammar_tool:main
	'''
)
