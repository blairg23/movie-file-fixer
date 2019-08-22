import os

for i in range(1, 100):
    filename = 'a' * i
    path = os.path.join('Fake_Directory', filename)
    os.chdir(path)
    os.mkdir(filename)
    filepath = "\\\\?\\" + os.path.join(os.getcwd(), path, filename)
    with open(filepath, 'a+') as outfile:
        outfile.write('blah')
