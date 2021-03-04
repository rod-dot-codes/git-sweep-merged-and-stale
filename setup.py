import sys
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

install_requires = [
    'GitPython>=3.1',
]

tag = "{tag}"
forced_tag = f"{os.environ.get('FORCED_TAG', '')}"

setup(name='git-sweep-merged-and-stale',
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
    packages=find_packages("src", exclude=["gitsweep.tests"]),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=['setuptools-git-versioning'],
    entry_points={
        'console_scripts':
            ['git-sweep-merged-and-stale=gitsweep.entrypoints:main']
    },
    version_config={
        "starting_version": forced_tag if forced_tag else tag
    },
)
