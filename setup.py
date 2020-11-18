import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nought", # Replace with your own username
    version="1.0.6",
		scripts=['bin/nought','bin/nt'],
		entry_points={
        'console_scripts': ['nought=nought.__main__:main'],
    },
    author="Cole Wilson",
    author_email="cole@colewilson.xyz",
    description="A super customizable file cleaner/organizer/automator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cole-wilson/nought",
    packages=setuptools.find_packages(),
		install_requires=[
   		'toml','requests'
		],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
		package_data={
      "": ["*.toml","*.txt"],
    },
		license="Apache-2.0",
		keywords='nought file organizer desktop cleaner declutterer devtools tools tool',
    project_urls={
        'Documentation': 'https://github.com/cole-wilson/nought',
        'Questions': 'https://github.com/cole-wilson/nought',
        'Source': 'https://github.com/cole-wilson/nought',
        'Tracker': 'https://github.com/cole-wilson/nought/issues',
    },
)
