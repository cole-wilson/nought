import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nought", # Replace with your own username
    version="1.0.1",
		# scripts=['bin/nought'],
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
   		'toml',
		],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
