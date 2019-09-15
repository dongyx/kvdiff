#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import argparse

__version__ = "0.2.1"

def main():
	try:
		parseargs()
		file1, file2 = args.filenames

		with open(file1, mode='rb') as fp1, \
			open(file2, mode='rb') as fp2, \
			external_sort(fp1) as sort1, \
			external_sort(fp2) as sort2:

			mergecmp(sort1.stdout, sort2.stdout)

		if sort1.returncode != 0 or sort2.returncode !=0:
			raise RuntimeError("sort(1) exits with non-zero code")

		return 0
		
	except Exception as e:
		raise
		print(e, file=sys.stderr)
		return -1

def parseargs():
	global args

	parser = argparse.ArgumentParser(
		description="Compare two text files by key columns",
		epilog="CAVEAT: The behavior is undefined if there're duplicated keys within a file")

	parser.add_argument(dest="filenames", metavar="FILENAME", nargs=2)

	parser.add_argument("-k", "--key", dest="keys", action="append",
		type=int, metavar="KEY", default=[1],
		help="specify the KEY-th column as one of the key columns; can be specified multiple times\n(default: 1)")

	parser.add_argument("-d", "--delimiter", dest="delimiter", action="store",
		metavar="DELIMITER", default=' ',
		help="use DELIMITER as the field separator character\n(default: the blank character)")

	parser.add_argument("-l", "--line", action="store_true",
		help="print the modified record in one line") 

	parser.add_argument("--version", action="version", version="%(prog)s " + __version__)

	args = parser.parse_args()

	if len(args.delimiter) != 1:
		raise ValueError("DELIMITER must be a character")

def external_sort(fp):
	sort_cmd = sum([["-k{0},{0}".format(str(key))] for key in args.keys], ["sort", "-u", "-t", args.delimiter])

	try:
		return subprocess.Popen(sort_cmd,
			stdin=fp, stdout=subprocess.PIPE, universal_newlines=True)

	except FileNotFoundError:
		raise FileNotFoundError("sort(1) must be installed")

def mergecmp(fp1, fp2):
	record1 = readline(fp1)
	record2 = readline(fp2)

	while record1 and record2:

		keys1 = getkeys(record1)
		keys2 = getkeys(record2)

		if keys2 < keys1:
			printadded(record2)
			record2 = readline(fp2)

		elif keys2 > keys1:
			printdeleted(record1)
			record1 = readline(fp1)

		else:
			if record1 != record2:
				printchanged(record1, record2)
			record1 = readline(fp1)
			record2 = readline(fp2)

	while record1:
		printdeleted(record1)
		record1 = readline(fp1)

	while record2:
		printadded(record2)
		record2 = readline(fp2)


def readline(fp):
	"""
	a line is either a str with '\n' or None, so after splitting, the last key will be (KEYS[-1] + '\n')
	if the file ends without '\n', '\n' will be added to the last line
	NOTE: some sort(1) implements will always output '\n' at the end of file whether the original file contains '\n' at the end
	"""

	line = fp.readline()

	if not line: return None

	if line[-1] != '\n':
		line += '\n'
	return line

def getkeys(line):
	columns = line.split(args.delimiter)
	return [columns[i - 1] for i in args.keys]

def output(*s):
	return print(*s, end='')

def printadded(line):
	output('+', line)

def printdeleted(line):
	output('-', line)

def printchanged(original, changed):
	if args.line:
		output('*', original.rstrip('\n'), '>', changed)
	else:
		output('*', original)
		output('>', changed)

if __name__ == "__main__":
	exit(main())
