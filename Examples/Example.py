# Example file for using lensIQ

import logging as log
import lensIQ
import lensIQ.defaultCalData

def app():
    # read the default lens data
    defaultData = lensIQ.defaultCalData.loadDefaultData("TW90")

    # initialize lensIQ
    IQ = lensIQ.lensIQ()
    IQ.loadData(defaultData)

    # calculate zoom step for focal length 15mm
    # Note: calculated focal length may not exactly match requested focal length due to zoom motor step size. 
    FL = 15
    zoomStep, err = IQ.FL2ZoomStep(FL)
    log.info(f'Calculate for {FL}mm focal length, unknown object distance: ')
    log.info(f'Zoom step {zoomStep} for {FL}mm focal length (error value: {err})')

    # update all lens configuration data
    IQ.updateAfterZoom(zoomStep)
    log.info(f'Updated parameters for FL {FL}mm but unknown object distance')
    printConfig(IQ)

    # calculate the best focus step for zoom 15mm and 10m object distance
    # Note: calcualted object distance may not match requested object distance due to limited number of steps in the focus motor.  
    #  for example, try 10.1 to see the difference 1 focus motor step makes.  
    objectDist = 10
    focusStep, err = IQ.OD2FocusStep(objectDist, zoomStep)
    log.info(f'Calculate for {objectDist}m object distance')
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
        log.info(f'  {f} = {IQ.lensConfiguration[f]["value"]:0.2f} (ts {IQ.lensConfiguration[f]["ts"]})')
    for f in ['zoomStep', 'focusStep', 'irisStep']:
        log.info(f'  {f} = {IQ.lensConfiguration[f]["value"]} (ts {IQ.lensConfiguration[f]["ts"]})')
    log.info('---')

log.basicConfig(level=log.DEBUG, format='%(levelname)-7s ln:%(lineno)-4d %(module)-18s  %(message)s')
if __name__ == '__main__':
    app()