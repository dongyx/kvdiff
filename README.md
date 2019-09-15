# KVDiff

Compare two text files by key columns

# Getting Started

Let's say we have two text files maintaining a list of systems with versions.

```
$ cat a.txt
MacOS 10.12
Windows 10
Ubuntu 16
```

```
$ cat b.txt
MacOS 10.14
Windows 10
Manjaro 17
```

To see which systems are new in `b.txt`, deleted in `b.txt`, and version changed in `b.txt`, run `kvdiff -k1 a.txt b.txt` in the terminal:

```
$ kvdiff -k1 a.txt b.txt
* MacOS 10.12
> MacOS 10.14
+ Manjaro 17
- Ubuntu 16
```

KVDiff reports that MacOS has a version change, new system Manjaro with version 17 is added, and Ubuntu is deleted.

# Requirements

+ Python >=3.5
+ [sort(1)](http://man7.org/linux/man-pages/man1/sort.1.html)

# Installation

	$ pip install kvdiff

# Usage

Run `kvdiff --help` for more infomation

# License

MIT licensed

# How It Works

[KVDiff: Compare Two Large Text Files by Key Columns](http://yxdong.me/posts/kvdiff.html)
