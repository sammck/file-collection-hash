from file_collection_hash import __version__ as library_version

# The following is automatically updated by semantic-release
_file_collection_hash_version = '0.1.0'

def test_version():
    assert library_version == _file_collection_hash_version
