#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import random
import string

CHARS = string.ascii_letters + string.digits
CWIDTH = 8

def main():
	try:
		parseargs()
		inputfiles = [open(f, 'w') for f in args.inputfiles]
		outputfile = open(args.outputfile, 'w')

		with inputfiles[0], inputfiles[1], outputfile:
			for r in genrecs():
				# appears in the first input file
				if random.randrange(2):
					print(r, file=inputfiles[0])

					# appears in the second input file
					if random.randrange(2):
						changed = None
						if random.randrange(2):
							changed = disturb(r)

						if changed:
							print(changed, file=inputfiles[1])
							print("*", r, ">", changed, file=outputfile)
						else:
							print(r, file=inputfiles[1])
					else:
						print("-", r, file=outputfile)
				else:
					# appears in the second input file
					if random.randrange(2):
						print(r, file=inputfiles[1])
						print("+", r, file=outputfile)
		return 0

	except Exception as e:
		raise
		print(e, file=sys.stderr)
		return -1

def disturb(r):
	split = r.split(args.d)
	i = min([i for i in range(args.m) if i not in args.k])
	while True:
		c = gencol()
		if split[i] != c:
			split[i] = c
			break
	return args.d.join(split)

def genrecs():
	keys = set()
	for _ in range(args.n):
		while True:
			r = args.d.join([gencol() for _ in range(args.m)])
			k = getkeys(r)
			if k not in keys:
				keys.add(k)
				break
		yield r

def gencol():
	return "".join([random.choice(CHARS) for _ in range(random.randint(1, CWIDTH))])

def getkeys(r):
	columns = r.split(args.d)
	return args.d.join([columns[i - 1] for i in args.k])

def parseargs():
	global args

	parser = argparse.ArgumentParser(description="Generate tests for KVDiff");
	parser.add_argument("inputfiles", metavar="inputfile", nargs=2)
	parser.add_argument("outputfile")
	parser.add_argument("-n", type=int, help="specify the number of records")
	parser.add_argument("-m", type=int, help="specify the number of columns")
	parser.add_argument("-d", default=" ",
		help="specify D as the delimiter; the default is the space")
	parser.add_argument("-k", type=int, action="append",
		help="specify the K-th column as a key column; can specify multiple times")

	args = parser.parse_args()
	args.k = [k - 1 for k in args.k]
	if args.n < 0 or args.m < 0 or 1 != len(args.d) \
		or any([ k < 0 or k > args.m for k in args.k]):
		raise ValueError("Wrong arguments")

if __name__ == "__main__":
	exit(main())
