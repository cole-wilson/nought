import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nought", # Replace with your own username
    version="0.0.2",
		scripts=['bin/nought'],
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
        "License :: OSI Approved :: Apache 2.0 License",
    ],
    python_requires='>=3.6',
)