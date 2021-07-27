import os
import subprocess

base_dir = 'F:\git_code'

def doGit():
    subprocess.call(['git', 'add', '*'])
    subprocess.call(['git', 'commit', '-am', '//tick sync'])
    subprocess.call(['git', 'push'])
    subprocess.call(['git', 'status'])

if __name__ == "__main__":
	list = os.listdir(base_dir)
	for it in list:
		if it[0] == '.':
			continue
		os.chdir(base_dir + '\\' + it)
		doGit()
