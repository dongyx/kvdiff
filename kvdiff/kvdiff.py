#!/usr/env/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import argparse

__version__ = "0.0.4"

def main():
	try:
		parseargs()
		file1, file2 = args.filenames
		sort_cmd = sum([["-k{0},{0}".format(str(key))] for key in args.keys], ["sort", "-u", "-t", args.delimiter])

		with open(file1, mode='r') as fp1, \
			open(file2, mode='r') as fp2, \
			subprocess.Popen(sort_cmd, stdin=fp1, stdout=subprocess.PIPE, text=True, encoding="UTF-8") as proc1, \
			subprocess.Popen(sort_cmd, stdin=fp2, stdout=subprocess.PIPE, text=True, encoding="UTF-8") as proc2:

			mergecmp(proc1.stdout, proc2.stdout)

		return 0
	except Exception as e:
		print(e, file=sys.stderr)
		return -1

def parseargs():
	global parser, args

	parser = argparse.ArgumentParser(
		description="Compare two text files by key columns",
		epilog="CAVEAT: The behavior is undefined if there're duplicated keys within a file")

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


def mergecmp(fp1, fp2):
	record1 = fp1.readline()
	record2 = fp2.readline()

	while record1 and record2:

		keys1 = getkeys(record1)
		keys2 = getkeys(record2)

		if keys2 < keys1:
			printadded(record2)
			record2 = fp2.readline()

		elif keys2 > keys1:
			printdeleted(record1)
			record1 = fp1.readline()

		else:
			if record1 != record2:
				printchanged(record1, record2)
			record1 = fp1.readline()
			record2 = fp2.readline()

	while record1:
		printdeleted(record1)
		record1 = fp1.readline()

	while record2:
		printadded(record2)
		record2 = fp2.readline()

def getkeys(line):
	columns = line.split(args.delimiter)
	return [columns[i - 1] for i in args.keys]

def printadded(line):
	print('+', line, end='')

def printdeleted(line):
	print('-', line, end='')

def printchanged(original, changed):
	print('*', original, end='')
	print('>', changed, end='')

if __name__ == "__main__":
	exit(main())
