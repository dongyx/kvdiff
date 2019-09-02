#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import subprocess

class TestAll(unittest.TestCase):
	def testall(self):
		return subprocess.run(["bash", "tests/test.sh"],
			stdin=subprocess.DEVNULL,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			check=True
		)
