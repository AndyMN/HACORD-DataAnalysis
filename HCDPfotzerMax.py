from HCDDataReader import HCDDataReader
from HCDDataProcessor import HCDDataProcessor
import pylab
import numpy as np

pressure_binsize = 0.5

##############################################################################################
########      BEXUS   ############
print "BEXUS"
BEXUS_reader = HCDDataReader("./Datasets/BEXUSDetectorFlightData")
BEXUS_processor = HCDDataProcessor()
BEXUS_data = BEXUS_processor.remove_peaks(BEXUS_reader.data)

pressure1_BX = BEXUS_data["press1"]
pressure2_BX = BEXUS_data["press2"]
pressure3_BX = BEXUS_data["press3"]
loop_time_BX = BEXUS_data["looptimer"]
HV_state_BX = BEXUS_data["hvstate"]
eth_state_BX = BEXUS_data["ethstate"]

gm1_BX_raw = np.array(BEXUS_data["gm1"])
gm2_BX_raw = np.array(BEXUS_data["gm2"])
gm3_BX_raw = np.array(BEXUS_data["gm3"])
gm4_BX_raw = np.array(BEXUS_data["gm4"])

gm1_BX = BEXUS_processor.datacut_based_on_statedata(gm1_BX_raw, HV_state_BX)
gm2_BX = BEXUS_processor.datacut_based_on_statedata(gm2_BX_raw, HV_state_BX)
gm3_BX = BEXUS_processor.datacut_based_on_statedata(gm3_BX_raw, HV_state_BX)
gm4_BX = BEXUS_processor.datacut_based_on_statedata(gm4_BX_raw, HV_state_BX)

mean_pressures_BX = []
for i, time in enumerate(pressure1_BX):
    if HV_state_BX[i] == 0:
        mean_pressure = (pressure1_BX[i] + pressure2_BX[i] + pressure3_BX[i]) / 3
        mean_pressures_BX.append(mean_pressure)

gm1_BX_average, gm1_BX_error, gm1_BX_binpoints = BEXUS_processor.average_counts_over_pressure(gm1_BX, mean_pressures_BX, binsize=pressure_binsize)
gm2_BX_average, gm2_BX_error, gm2_BX_binpoints = BEXUS_processor.average_counts_over_pressure(gm2_BX, mean_pressures_BX, binsize=pressure_binsize)
gm3_BX_average, gm3_BX_error, gm3_BX_binpoints = BEXUS_processor.average_counts_over_pressure(gm3_BX, mean_pressures_BX, binsize=pressure_binsize)
gm4_BX_average, gm4_BX_error, gm_4_BX_binpoints = BEXUS_processor.average_counts_over_pressure(gm4_BX, mean_pressures_BX, binsize=pressure_binsize)



pressures_BX_average, pressures_BX_error = BEXUS_processor.pressurebin_centers(mean_pressures_BX, binsize=pressure_binsize)
gm_BX_weighted_average, gm_BX_weighted_error = BEXUS_processor.weighted_average([gm1_BX_average, gm2_BX_average, gm3_BX_average, gm4_BX_average], [gm1_BX_error, gm2_BX_error, gm3_BX_error, gm4_BX_error])

#####################################################################################################################


