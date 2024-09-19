# Example file for using lensIQ
# (updated for v.1.5.0)

import logging
import lensIQ
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
import json


def app():
    # read the default lens data
    def openFile():
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename(defaultextension='.json', filetypes=[('JSON File', '.json')], title="Open data files") # show an "Open" dialog box and return the path to the selected file
        log.info("Opening lens data file: {}".format(filename))

        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    defaultData = openFile()

    # initialize lensIQ
    IQ = lensIQ.lensIQ(debugLog=True)
    IQ.loadData(defaultData)

    # calculate zoom step for focal length 15mm
    # Note: calculated focal length may not exactly match requested focal length due to zoom motor step size. 
    FL = 15
    log.info(f'Calculate for {FL}mm focal length, unknown object distance: ')
    zoomStep, err = IQ.FL2ZoomStep(FL)
    log.info(f'Zoom step {zoomStep} for {FL}mm focal length (error value: {err})')

    # update all lens configuration data
    IQ.updateAfterZoom(zoomStep)
    log.info(f'Updated parameters for FL {FL}mm but unknown object distance')
    printConfig(IQ)

    # calculate the best focus step for zoom 15mm and 10m object distance
    # Note: calcualted object distance may not match requested object distance due to limited number of steps in the focus motor.  
    #  for example, try 10.1 to see the difference 1 focus motor step makes.  
    objectDist = 10
    log.info(f'Calculate for {objectDist}m object distance')
    focusStep, err = IQ.OD2FocusStep(objectDist, zoomStep)
    log.info(f'Focus step {focusStep} for object distance {objectDist}m at {FL}mm focal length (error value: {err})')

    # udpate all lens configuration data
    IQ.updateAfterFocus(focusStep)
    log.info(f'Updated parameters at object distance {objectDist}m')
    printConfig(IQ)

    # reduce the aperture to F/4
    # At closer object distance, this will have a noticable effect on the DOF calcualtion. 
    fNum = 4
    irisStep, err = IQ.fNum2IrisStep(fNum, FL)
    log.info(f'Calculate at a smaller aperture f{fNum}')
    log.info(f'Iris step {irisStep} for F/{fNum} (error value: {err})')

    # update all lens configuration data
    IQ.updateAfterIris(irisStep)
    log.info(f'Updated parameters for F/{fNum}')
    printConfig(IQ)

def printConfig(IQ):
    for f in ['AOV', 'FOV', 'DOF', 'FL', 'OD', 'FNum', 'NA']:
        log.info(f'  {f} = {IQ.engValues[f]["value"]:0.2f} (ts {IQ.engValues[f]["ts"]})')
    for f in ['zoomStep', 'focusStep', 'irisStep']:
        log.info(f'  {f} = {IQ.engValues[f]["value"]} (ts {IQ.engValues[f]["ts"]})')
    log.info('---')

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-7s ln:%(lineno)-4d %(module)-18s  %(message)s')
if __name__ == '__main__':
    app()