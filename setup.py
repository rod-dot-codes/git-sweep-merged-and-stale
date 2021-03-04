import sys
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

version = '0.2'

install_requires = [
    'GitPython>=0.3.2RC1',
    'freezegun',
    'pytest',
    'mock'
]

# Add argparse if less than Python 2.7
if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
    install_requires.append('argparse>=1.2.1')

setup(name='git-sweep-merged-and-stale',
    version=version,
    description="Clean up branches from your Git remotes",
    long_description=README,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Version Control',
        'Topic :: Text Processing'
    ],
    keywords='git maintenance branches merge stale',
    author='Rodney Hawkins',
    author_email='rodneyhawkins@gmail.com',
    url='http://rod.codes',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['git-sweep-merged-and-stale=gitsweep.entrypoints:main']
    }
)
