#!/usr/env/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import tempfile
import argparse
from argparse import ArgumentDefaultsHelpFormatter

__version__ = "0.0.3"

def main():
	try:
		parseargs()
		file1, file2 = args.filenames

		with open(file1, mode='r') as fp1, \
			open(file2, mode='r') as fp2, \
			tempfile.TemporaryFile("w+") as sorted_fp1, \
			tempfile.TemporaryFile("w+") as sorted_fp2:

			sort_args = ["-u", "-t", args.delimiter] \
				+ sum([["-k", str(key)] for key in args.keys], [])

			external_sort(fp1, sorted_fp1, sort_args)
			external_sort(fp2, sorted_fp2, sort_args)

			sorted_fp1.seek(0)
			sorted_fp2.seek(0)

			mergecmp(sorted_fp1, sorted_fp2)

		return 0
	except Exception as e:
		print(e, file=sys.stderr)
		return -1

def parseargs():
	global parser, args

	parser = argparse.ArgumentParser(
		description="Compare two text files by key columns",
		epilog="CAVEAT: The behavior is undefined if there're duplicated keys within a file\n\n \
		\nAuthor: Yuxuan Dong")

	parser.add_argument(dest="filenames", metavar="FILENAME", nargs=2)

	parser.add_argument("-k", "--key", dest="keys", action="append",
		type=int, metavar="KEY", required=True,
		help="specify the KEY-th column as one of the key columns; can be specified multiple times")

	parser.add_argument("-d", "--delimiter", dest="delimiter", action="store",
		metavar="DELIMITER", default=' ',
		help="use DELIMITER as the field separator character\n(default: the blank character)")

	parser.add_argument("--version", action="version", version="%(prog)s " + __version__)

	args = parser.parse_args()

	if len(args.delimiter) != 1:
		raise ValueError("DELIMITER must be a character")

def external_sort(infp, outfp, args):
	try:
		return subprocess.run(["sort"] + args,
			stdin=infp, stdout=outfp, check=True)
	except FileNotFoundError:
		raise FileNotFoundError("The sort utility must be installed on the system")

def mergecmp(fp1, fp2):
	buf1 = fp1.readline()
	buf2 = fp2.readline()

	while buf1 and buf2:
		record1 = rstrip(buf1)
		record2 = rstrip(buf2)

		keys1 = getkeys(record1)
		keys2 = getkeys(record2)

		if keys2 < keys1:
			printadded(record2)
			buf2 = fp2.readline()

		elif keys2 > keys1:
			printdeleted(record1)
			buf1 = fp1.readline()

		else:
			if record1 != record2:
				printchanged(record1, record2)
			buf1 = fp1.readline()
			buf2 = fp2.readline()

	if buf1:
		printdeleted(rstrip(buf1))
	for line in fp1:
		printdeleted(rstrip(line))

	if buf2:
		printadded(rstrip(buf2))
	for line in fp2:
		printadded(rstrip(line))

def getkeys(line):
	columns = line.split(args.delimiter)
	return [columns[i - 1] for i in args.keys]

def rstrip(s):
	return s.rstrip("\n")

def printadded(line):
	print('+', line)

def printdeleted(line):
	print('-', line)

def printchanged(original, changed):
	print('*', original)
	print('>', changed)

if __name__ == "__main__":
	exit(main())
