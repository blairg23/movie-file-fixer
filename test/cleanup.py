import os
import shutil

current_path, filename= os.path.split(os.path.abspath(__file__)) # To start us in the correct directory		

cleanup_folders = [os.path.join(current_path, 'data', 'Fake_Directory')]
for folder in cleanup_folders:
	if os.path.exists(folder):
		shutil.rmtree(folder)