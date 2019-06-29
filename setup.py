import setuptools
import sys
import os

with open("README.md", 'r') as fp:
	longdesc = fp.read()

setuptools.setup(
	name="kvdiff",
	version="0.0.0",
	author="Yuxuan Dong",
	author_email="yuxuan.dong@outlook.com",
	description="Compare two text files by key columns",
	long_description=longdesc,
	long_description_content_type="text/markdown",
	url="https://github.com/dongyx/kvdiff",
	packages=setuptools.find_packages(),
	entry_points={
		"console_scripts": [
			"kvdiff=kvdiff.kvdiff:main"
		]
	},

	python_requires=">=3.5",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX"
	]
)
