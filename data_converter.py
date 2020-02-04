from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt

#Define input file and it's shape.
#For now this has to be done manually for each file.
filename = '../force-1-2048-28,68'
shape = (2048, 2048)

#Load file
tiff = Image.open(filename)
tiff.seek(0)
A = np.array(tiff.getdata())

#Find correct channel
#Right now it is set to 'vDeflection'. This also has to be done manually
for image in range(tiff.n_frames - 1):
    tiff.seek(image)

    for item in tiff.tag_v2.items():

        if item[0] == 32851:
            if item[1].find('vDeflection') != -1:
                if item[1].find('retrace : false') != -1:
                    A = np.array(tiff.getdata())
                    for item in tiff.tag_v2.items():
                        if item[0] == 33076:
                            a = item[1]
                        if item[0] == 33077:
                            b = item[1]
                    A = A*a + b

                if item[1].find('retrace : true') != -1:
                    tiff.seek(0)
                    B = np.array(tiff.getdata())
                    tiff.seek(image)
                    B = np.array(tiff.getdata())
                    for item in tiff.tag_v2.items():
                        if item[0] == 33076:
                            a = item[1]
                        if item[0] == 33077:
                            b = item[1]
                    B = B*a + b

#Array reshape
a1 = np.reshape(A, shape)
b1 = np.reshape(B, shape)
b1 = np.flip(b1, axis = 1)
a1b1 = np.append(a1, b1, axis=1)
a1b1 = np.flip(a1b1, axis = 0)
a1b1 = a1b1.reshape(-1)

#Plot figure if you want.
plt.figure()
plt.plot(a1b1)
plt.show()

#Save file
np.save(filename + "_converted1.npy", a1b1)
