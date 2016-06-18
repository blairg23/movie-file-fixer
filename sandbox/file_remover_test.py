from datetime import datetime
import os
def scandirs(path):
    for root, dirs, files in os.walk(path):
        for currentFile in files:
            print "processing file: " + currentFile
            exts=['.nfo', '.dat', '.jpg', '.png', '.txt']
            if any(currentFile.lower().endswith(ext) for ext in exts):
                os.remove(os.path.join(root, currentFile))

def remove_files(directory=None, extensions=['.nfo', '.dat', '.jpg', '.png', '.txt']):
		for root, dirs, files in os.walk(directory):
			for current_file in files:
				print '[Processing File: {filename}]'.format(filename=current_file)
				filename, ext = os.path.splitext(current_file)
				if ext in extensions:
					os.remove(os.path.join(root, current_file))   



# These are identical copies of each other
dir1 = os.path.join('data', 'Fake_Directory')
dir2 = os.path.join('data', 'Fake_Directory2')

print 'Running scandirs()'
start = datetime.now()
scandirs(dir1)
finish = datetime.now() - start
print 'Finished. Time=', finish

print 'Running remove_files()'
start = datetime.now()
remove_files(directory=dir2)
finish = datetime.now() - start
print 'Finished. Time=', finish