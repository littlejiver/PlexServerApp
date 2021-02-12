import os

filesArray = []

for root, dirs, files in os.walk("/media/HDD1/PlexContent/Movies"):
    for file in files:
        os.rename(root + "/" + file, root + "/" + file.replace(".", " ", file.count(".")-1))

for x in filesArray:
    print(x)

