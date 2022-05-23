#!/usr/bin/env python3

import os
from file_collection_hash import file_collection_hash

print(file_collection_hash(exclude=['.git', '.venv']))
print(file_collection_hash('scripts'))
print(file_collection_hash('scripts', ignore_owner=False, ignore_group=False))
os.chdir('scripts')
print(file_collection_hash())
