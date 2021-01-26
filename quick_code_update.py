import os
folderroot = '~/NOT_Reductions/'
os.chdir(folderroot)
import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
import shutil

import sys
from pyraf import iraf
iraf.noao(_doprint=0)
iraf.imred(_doprint=0)
iraf.ccdred(_doprint=0)
iraf.twodspec(_doprint=0)
iraf.longslit(_doprint=0)
iraf.kpnoslit(_doprint=0)
iraf.astutil(_doprint=0)
iraf.onedspec(_doprint=0)
iraf.twodspec.longslit.dispaxis = 2

#read object keywords
for file in os.listdir(os.getcwd()):
    if file.endswith('.fits'):
        testfile = file
        shutil.copy(file,'./original/.')


hduo = fits.open(testfile)

#name targets (science & standard)
target = hduo[0].header['OBJECT']
#target2 = 'SP0644p375'
#std = 'SP0305+261'

#create list of science files
sci = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.fits'):
        sci.append(file+'[1]')


file1 = open('listasci', 'w')
file1.writelines(["%s\n" % item  for item in sci])
file1.close()

#copy calib files in the current dir
shutil.copy(folderroot+'bias/bias.fits', folderroot)
shutil.copy(folderroot+'flat/response.fits', folderroot)

#Subtract bias
iraf.imarith('@listasci', '-', 'bias.fits', '@listasci//_2b')

#flat subtraction
iraf.imarith('*_2b.fits', '/', 'response.fits', '@listasci//_2bf')

#SCIENCE
#APALL
iraf.imred.kpnoslit
final = []
for file in os.listdir(os.getcwd()):
    if file.endswith('2bf.fits'):
        final.append(file)


file1 = open('listafinal', 'w')
file1.writelines(["%s\n" % item  for item in final])
file1.close()

f = open('listafinal')
i = 1
for item in f:
    print item
    file = item.split('\n')[0]
    shutil.copy(file, 'spec'+str(i)+'.fits')
    i += 1


#assign 2d dispersion solution - from now IRAF
iraf.noao.twodspec.longslit
for file in os.listdir(os.getcwd()):
    if file.startswith('spec'):
        iraf.transform(file,output='w'+file,database="wavelength",fitnames="He_Ne_ThAr_bsHe_Ne_ThAr_bs",flux='yes')

#minor tweak to wavelength solution

iraf.hedit('wspec*.fits',fields='CRVAL2',value='2573.5979',verify='no',show='no')

#
#FROM NOW -> iraf
iraf.noao.twodspec.apextract
iraf.apall('wspec*.fits',interactive = 'yes',line=800,t_function = "legendre",t_order = 2, b_order=2, background="fit", skybox=1, pfit="fit1d" )


###wavelength calinration
##for file in os.listdir(os.getcwd()):
##    if file.endswith('ms.fits'):
##        iraf.dispcor(file, 'd'+file)
#
#
#flux calibration
shutil.copy('./stds/sens.0001.fits','./sens.fits')
shutil.copy('./stds/lapalmaextinct.dat','.')
#
#
for file in os.listdir(os.getcwd()):
    if file.startswith('wspec'):
        if file.endswith('ms.fits'):
            iraf.calibrate(file, 'f'+file)
#
#combine spectra
finalcomb = []
for file in os.listdir(os.getcwd()):
    if file.startswith('fws'):
        finalcomb.append(file)


file1 = open('listascombine', 'w')
file1.writelines(["%s\n" % item  for item in finalcomb])
file1.close()
#
iraf.scombine('@listascombine', 'temp_quick.fits')

iraf.scopy('temp_quick.fits',target+'_quick.fits',w1='3800',w2='9000')

iraf.wspectext(target+'_quick.fits',target+'_spec.txt',header='no')

#mv final file in a dedicated folder
shutil.copy(target+'_quick.fits','./output/.')
shutil.copy(target+'_spec.txt','./output/.')
#
#remove temp FILES
os.remove('lapalmaextinct.dat')
os.remove(target+'_spec.txt')
for file in os.listdir(os.getcwd()):
    if file.endswith('fits'):
        os.remove(file)
    elif file.startswith('lista'):
        os.remove(file)
    elif file.startswith('log'):
        os.remove(file)
#
#
shutil.rmtree('database')
##
