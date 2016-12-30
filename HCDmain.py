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


#######################################################################################################################
################      KMI    ##################
print "KMI"
KMI_reader = HCDDataReader("./Datasets/KMI102014", software_version=1)
KMI_processor = HCDDataProcessor()
KMI_processor.remove_peaks(KMI_reader.data)

pressure_KMI = KMI_reader.data["press1"]
gm1_KMI = np.array(KMI_reader.data["gm1"])
gm2_KMI = np.array(KMI_reader.data["gm2"])
gm3_KMI = np.array(KMI_reader.data["gm3"])
gm4_KMI = np.array(KMI_reader.data["gm4"])


gm1_KMI_average, gm1_KMI_error, gm1_KMI_binpoints = KMI_processor.average_counts_over_pressure(gm1_KMI, pressure_KMI, binsize=pressure_binsize)
gm2_KMI_average, gm2_KMI_error, gm2_KMI_binpoints = KMI_processor.average_counts_over_pressure(gm2_KMI, pressure_KMI, binsize=pressure_binsize)
gm3_KMI_average, gm3_KMI_error, gm3_KMI_binpoints = KMI_processor.average_counts_over_pressure(gm3_KMI, pressure_KMI, binsize=pressure_binsize)
gm4_KMI_average, gm4_KMI_error, gm4_KMI_binpoints = KMI_processor.average_counts_over_pressure(gm4_KMI, pressure_KMI, binsize=pressure_binsize)
pressures_KMI_average, pressures_KMI_error = KMI_processor.pressurebin_centers(pressure_KMI, binsize=pressure_binsize)


gm_KMI_weighted_average, gm_KMI_weighted_error = KMI_processor.weighted_average([gm1_KMI_average, gm2_KMI_average, gm3_KMI_average, gm4_KMI_average], [gm1_KMI_error, gm2_KMI_error, gm3_KMI_error, gm4_KMI_error])

################################################################################################################
############################################## KNMI 04-2015 ####################################################################
KNMI_reader = HCDDataReader("./Datasets/KNMI042015", software_version=2)
KNMI_processor = HCDDataProcessor()
KNMI_processor.remove_peaks(KNMI_reader.data)

pressure_KNMI = KNMI_reader.data["press1"]
gm1_KNMI = np.array(KNMI_reader.data["gm1"])
gm2_KNMI = np.array(KNMI_reader.data["gm2"])
gm3_KNMI = np.array(KNMI_reader.data["gm3"])
gm4_KNMI = np.array(KNMI_reader.data["gm4"])


gm1_KNMI_average, gm1_KNMI_error, gm1_KNMI_binpoints = KNMI_processor.average_counts_over_pressure(gm1_KNMI, pressure_KNMI, binsize=pressure_binsize)
gm2_KNMI_average, gm2_KNMI_error, gm2_KNMI_binpoints = KNMI_processor.average_counts_over_pressure(gm2_KNMI, pressure_KNMI, binsize=pressure_binsize)
gm3_KNMI_average, gm3_KNMI_error, gm3_KNMI_binpoints = KNMI_processor.average_counts_over_pressure(gm3_KNMI, pressure_KNMI, binsize=pressure_binsize)
gm4_KNMI_average, gm4_KNMI_error, gm4_KNMI_binpoints = KNMI_processor.average_counts_over_pressure(gm4_KNMI, pressure_KNMI, binsize=pressure_binsize)


pressures_KNMI_average, pressures_KNMI_error = KNMI_processor.pressurebin_centers(pressure_KNMI, binsize=pressure_binsize)
gm_KNMI_weighted_average, gm_KNMI_weighted_error = KNMI_processor.weighted_average([gm1_KNMI_average, gm2_KNMI_average, gm3_KNMI_average, gm4_KNMI_average], [gm1_KNMI_error, gm2_KNMI_error, gm3_KNMI_error, gm4_KNMI_error])



fig = pylab.figure(1)
ax = fig.add_subplot(1, 1, 1)
ax.errorbar(pressures_BX_average, gm_BX_weighted_average, yerr=gm_BX_weighted_error, fmt='o')
ax.errorbar(pressures_KMI_average, gm_KMI_weighted_average, yerr=gm_KMI_weighted_error, fmt='*')
ax.errorbar(pressures_KNMI_average, gm_KNMI_weighted_average, yerr=gm_KNMI_weighted_error, fmt='x')
ax.set_xscale('log')
ax.set_xlim([1, 100])
ax.set_ylim([0, 45])
pylab.rcParams["legend.numpoints"] = 1
#pylab.rcParams.update({'font.size': 22})
pylab.grid(True)
pylab.xlabel("Atmospheric pressure (kPa)")
pylab.ylabel("Flux (counts/s)")
pylab.legend(["BEXUS", "RMIB", "RMIN"])
pylab.savefig("totalcounts_compared_05kPa_binsize.png", dpi=1200)

pylab.show()
