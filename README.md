file-collection-hash: Generate stable hash of a directory or 
=================================================

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Latest release](https://img.shields.io/github/v/release/sammck/file-collection-hash.svg?style=flat-square&color=b44e88)](https://github.com/sammck/pulumi-crypto/releases)

A Python commandline tool and callable function that can efficiently compute a repeatable hash
string for the content of a directory or a collection of files.



Table of contents
-----------------

* [Introduction](#introduction)
* [Details](#pulumi-passphrase-encryption-details)
* [Installation](#installation)
* [Usage](#usage)
  * [Command line](#command-line)
  * [API](api)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)


Introduction
------------

Python package `file-collection-hash` provides a command-line tool as well as a runtime function to efficiently
generate a stable content hash for a directory or collection of files. In general, a directory created
with `rsync -a old_dir/ new_dir/` will produce the same hash. The hash includes the data of
all files, so it is reliable regardless of file timestamps, etc.

Files within a directory are processed in alhabetically sorted order, so that hashes remain stable across directory
reconstruction.

Relative pathnames are included in the path, so that if a file is renamed, the hash will change.

By default, file modify timestamps, file owner/UID, and file group/GID are ignored for the purposes of hashing, so that
directories cloned onto different systems will hash the same even if a different user owns the directory
or UID/GID mappings are different. Options are provided to enabled includion of these properties in the hash.

By default, file permission/mode bits (e.g., Read, Write, Execute) are included in the hash; this allows applications
to recognize chmod operations as significant and requiring update.

In general, the default options produce a hash that changes under similar conditions to when `git status` would
show a change.

The hashing function can be any filter command that takes a byte stream as input and produces a whitespace-free
textual hash as output. Any output from the first whitespace on is stripped.

`file-collection-hash` delegates all of the heavy lifting to two very optimized native external commands, piped together:
1. `tar` is used to render all included files and directories into a repeatable byte stream. Command options
   on `tar` are used to sort the input files and to hide variations in owner, group, modify timestamps,
   and permission bits as required. The output of `tar` is piped directly into the hashing filter.
2. The hashing filter command (by default `sha256sum`) has its stdin piped directly from the `tar` output.

This package was originally developed as part of a solution to update `.tar.gz` files, triggering dependent
actions, only when there is a material change in the content being bundled, ignoring differences in timestamp
and file owner/group settings.

Installation
------------

### Prerequisites

**Python**: Python 3.7+ is required. See your OS documentation for instructions.

### From PyPi

The current released version of `file-collection-hash` can be installed with 

```bash
pip3 install pulumi-crypto
```

### From GitHub

[Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) is required; it can be installed with:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Clone the repository and install pulumi-crypto into a private virtualenv with:

```bash
cd <parent-folder>
git clone https://github.com/sammck/file-collection-hash.git
cd file-collection-hash
poetry install
```

You can then launch a bash shell with the virtualenv activated using:

```bash
poetry shell
```

Usage
=====

Command Line
------------

Example usage:

```bash
$ file-collection-hash --exclude=.git --exclude=.venv
a25f091c7de730931480a97243a15cfce7cd0fe07eee925749e5dc37a573237e
$ file-collection-hash -C scripts
f039c1016394986afb86436e58a3708fcd375789f95f178c7c340e29f01cf637
$ file-collection-hash -C scripts --no-ignore-owner --no-ignore-group
bb6d86071992c01336eaaa05cf2fdb64896b339f4fcf048cda45fa2c12aa7db6
$ cd scripts
$ file-collection-hash
f039c1016394986afb86436e58a3708fcd375789f95f178c7c340e29f01cf637
```

API
---

```python
#!/usr/bin/env python3

import os
from file_collection_hash import file_collection_hash

print(file_collection_hash(exclude=['.git', '.venv']))
print(file_collection_hash('scripts'))
print(file_collection_hash('scripts', ignore_owner=False, ignore_group=False))
os.chdir('scripts')
print(file_collection_hash())
```

Known issues and limitations
----------------------------

* TBD.

Getting help
------------

Please report any problems/issues [here](https://github.com/sammck/file-collection-hash/issues).

Contributing
------------

Pull requests welcome.

License
-------

pulumi-crypto is distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT).  The license applies to this file and other files in the [GitHub repository](http://github.com/sammck/file-collection-hash) hosting this file.

Authors and history
---------------------------

The author of file-collection-hash is [Sam McKelvie](https://github.com/sammck).
