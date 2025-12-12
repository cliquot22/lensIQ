# This is for internal testing.  The BFL calibration data points are passed to the initialBFLValues function which
# does the fit.  Normally BFL values are selected by the user but these are already known.  
# (updated for v.1.5.0)

import logging
import lensIQ
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
import json

### From Theia_lensIQ_GUI
class BFLClass(): 
    SELECTED_POINT_MAX_DIST = 0.0007        # graph point selection maximum distance from selected point
    FIT_COLOR = 'green'
    SELECTED_COLOR = 'red'
    CURRENT_COLOR = 'light blue'
    '''
    This class creates a BFL calibration window.  The window will display the calibration points
    used for BFL calibration as focus step difference vs. focal length.  The window also displays and
    allows copying of the calibration function.  
    '''
    def __init__(self, lensIQ):
        '''
        Initialize the class
        ### input:
        - lensIQ: lensIQ module handle
        '''
        self.BFLWindow = None           # window handle
        self.graphPointID = []          # graph point ID values
        self.selectedPointID = 0        # selected point ID value
        self.fitID = []                 # graph fit curve ID value
        self.currentPointID = 0
        self.lensIQ = lensIQ

        self.xLimits = []               # graph limits (min, max, tick spacing)
        self.yLimits = []
        self.calibrationOD = 0

    # store the initial BFL values and calculate coefficients
    def initialBFLValues(self, BFLPoints:tuple=[]):
        '''
        Store the initial BFL values adn create the BFL coefficients if there are none alreay existing
        ### input:
        - BFLPoints (optional: []): list of correction points [[FL:mm, focus step delta:steps, OD:m],...]
        '''
        if BFLPoints and len(self.lensIQ.BFLCorrectionValues) == 0:
            log.info(f'Saving initial BFL correction points {BFLPoints}')
            for pt in BFLPoints:
                self.lensIQ.addBFLCorrectionDelta(pt[0], pt[1], pt[2])
            self.calibrationOD = self.lensIQ.BFLCorrectionValues[0][2]


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-7s ln:%(lineno)-4d %(module)-18s  %(message)s')

lensIQ = lensIQ.lensIQ()
BFL = BFLClass(lensIQ)

# read the default lens data
def openFile():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(defaultextension='.json', filetypes=[('JSON File', '.json')], title="Open data files") # show an "Open" dialog box and return the path to the selected file
    log.info("Opening lens data file: {}".format(filename))

    with open(filename, 'r') as f:
        data = json.load(f)
    return data
defaultData = openFile()

lensIQ.loadData(defaultData)
BFLValuesAveCal = [
    [46.0584305176243,-219.930009238369,2.5],
    [38.9823265477265,-87.8432872397962,2.5],
    [12.578181281477,99.2385581760536,2.5],
    [14.4065890562032,83.0549700118481,2.5],
    [15.9314090020057,-31.1168829878843,2.5],
    [29.5831900046469,-20.5824942708277,2.5],
    [20.9644431655279,80.5820573251551,2.5],
]
BFLValuesCal = [
    [46.0584305176243,-82.8564493595331,2.5],
    [38.9823265477265,-137.528271152063,2.5],
    [12.578181281477,-76.3984469224852,2.5],
    [14.4065890562032,-51.7079703382467,2.5],
    [15.9314090020057,-208.03632262819,2.5],
    [29.5831900046469,-67.3591082250892,2.5],
    [20.9644431655279,-64.7091910219768,2.5],
]
BFL.initialBFLValues(BFLValuesCal)

log.info(lensIQ.BFLCorrectionValues)
log.info(lensIQ.BFLCorrectionCoeffs)