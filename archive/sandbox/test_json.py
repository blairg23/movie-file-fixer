import json
import os

filename = 'I:\Dropbox\Projects\Python\MovieFilenameFixer\movie-file-fixer\data\Fake_Directory'
test_file = 'test_file.json'
test_path = os.path.join(filename, test_file)

with open(test_path, mode='r') as infile:
    test_dict = json.load(infile)
print
test_dict
