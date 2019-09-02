import setuptools

from src.kvdiff.kvdiff import __version__ as version

with open("README.md", 'r') as fp:
	longdesc = fp.read()

setuptools.setup(
	name="kvdiff",
	version=version,
	author="YuXuan Dong",
	author_email="yuxuan.dong@outlook.com",
	description="Compare two text files by key columns",
	long_description=longdesc,
	long_description_content_type="text/markdown",
	url="https://github.com/dongyx/kvdiff",
	license="MIT",
	python_requires=">=3.5",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX"
	],

	packages=setuptools.find_packages("src"),
	package_dir={ "": "src" },
	test_suite="tests",

	entry_points={
		"console_scripts": [
			"kvdiff=kvdiff.kvdiff:main"
		]
	}
)
