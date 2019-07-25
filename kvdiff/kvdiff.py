#!/usr/env/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import argparse
import locale
import os

__version__ = "0.0.4"

def main():
	try:
		parseargs()
		file1, file2 = args.filenames
		env = os.environ.copy()
		env['LC_ALL'] = args.encoding
		language_code, encoding = args.encoding.split('.')
		sort_cmd = sum([["-k{0},{0}".format(str(key))] for key in args.keys], ["sort", "-u", "-t", args.delimiter])

		with open(file1, mode='rb') as fp1, \
			open(file2, mode='rb') as fp2, \
			subprocess.Popen(sort_cmd, env=env, stdin=fp1, stdout=subprocess.PIPE, text=True, encoding=encoding) as proc1, \
			subprocess.Popen(sort_cmd, env=env, stdin=fp2, stdout=subprocess.PIPE, text=True, encoding=encoding) as proc2:

			mergecmp(proc1.stdout, proc2.stdout, encoding)

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

	parser.add_argument("-e", "--encoding", dest="encoding", action="store",
		metavar="ENCODING", default='.'.join(locale.getlocale(locale.LC_ALL)),
		help="use ENCODING as the file encoding\n")

	parser.add_argument("--version", action="version", version="%(prog)s " + __version__)

	args = parser.parse_args()

	if len(args.delimiter) != 1:
		raise ValueError("DELIMITER must be a character")


def mergecmp(fp1, fp2, outencoding):

	sys.stdout.reconfigure(encoding=outencoding)

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
	line is either str with '\n' or None, so after splitting, the last key will be (KEYS[-1] + '\n')
	if file end without '\n', '\n' will be added to the last line
	NOTE: some sort utility will always output '\n' at file end whether the original file contains '\n' at file end
	"""
	line = fp.readline()
	if not line: return None
	if line[-1] != '\n':
		line += '\n'
	return line

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
