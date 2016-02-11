from HCDDataReader import HCDDataReader
from HCDDataProcessor import HCDDataProcessor
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

pressure_binsize = 0.5


############################################## KMI 10-2014 ####################################################################
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

peak_boundaries_KMI = KMI_processor.set_peak_boundaries(xmin = 3.043499, xmax = 10.316913)
#peak_boundaries_KMI = KMI_processor.set_peak_boundaries(x=pressures_KMI_average, y=gm_KMI_weighted_average)
pressure_peak_KMI, gm_counts_peak_KMI, peak_points_KMI = KMI_processor.extract_peak([pressures_KMI_average, pressures_KMI_error], [gm_KMI_weighted_average, gm_KMI_weighted_error])
pfotzer_KMI, pfotzer_error_KMI = KMI_processor.pfotzer_max(pressure_peak_KMI, gm_counts_peak_KMI)

#print str(pfotzer_KMI) + " +- " + str(pfotzer_error_KMI)

xnew = np.arange(min(pressure_peak_KMI[0]), max(pressure_peak_KMI[0]), 0.01)
ynew_der = KMI_processor.derivative_peak_spline(xnew)
ynew = KMI_processor.peak_spline(xnew)



fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.errorbar(pressure_peak_KMI[0], gm_counts_peak_KMI[0], yerr=gm_counts_peak_KMI[1], fmt="o")
plt.plot(xnew, ynew)
plt.title('k = 4 spline interpolation')
plt.show()
########################################################################################################################
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

peak_boundaries_KNMI = KNMI_processor.set_peak_boundaries(xmin = 3.572474, xmax = 10.184669)
#peak_boundaries_KNMI = KNMI_processor.set_peak_boundaries(x=pressures_KNMI_average, y=gm_KNMI_weighted_average)
pressure_peak_KNMI, gm_counts_peak_KNMI, peak_points_KNMI = KNMI_processor.extract_peak([pressures_KNMI_average, pressures_KNMI_error], [gm_KNMI_weighted_average, gm_KNMI_weighted_error])
pfotzer_KNMI, pfotzer_error_KNMI = KNMI_processor.pfotzer_max(pressure_peak_KNMI, gm_counts_peak_KNMI)

#print str(pfotzer_KNMI) + " +- " + str(pfotzer_error_KNMI)

xnew2 = np.arange(min(pressure_peak_KNMI[0]), max(pressure_peak_KNMI[0]), 0.01)
ynew_der2 = KNMI_processor.derivative_peak_spline(xnew2)
ynew2 = KNMI_processor.peak_spline(xnew2)



#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.errorbar(pressure_peak_KNMI[0], gm_counts_peak_KNMI[0], yerr=gm_counts_peak_KNMI[1], fmt="o")
#plt.plot(xnew2, ynew2)
#plt.title('k = 4 spline interpolation')
#plt.show()
########################################################################################################################
############################################## KIRUNA ####################################################################
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


peak_boundaries_BX = BEXUS_processor.set_peak_boundaries(xmin = 0.873754, xmax = 7.485949)
#peak_boundaries_BX = BEXUS_processor.set_peak_boundaries(x=pressures_BX_average, y=gm_BX_weighted_average)
pressure_peak_BX, gm_counts_peak_BX, peak_points_BX = BEXUS_processor.extract_peak([pressures_BX_average, pressures_BX_error], [gm_BX_weighted_average, gm_BX_weighted_error])
pfotzer_BX, pfotzer_error_BX = BEXUS_processor.pfotzer_max(pressure_peak_BX, gm_counts_peak_BX)

#print str(pfotzer_BX) + " +- " + str(pfotzer_error_BX)

xnew3 = np.arange(min(pressure_peak_BX[0]), max(pressure_peak_BX[0]), 0.01)
ynew_der3 = BEXUS_processor.derivative_peak_spline(xnew3)
ynew3 = BEXUS_processor.peak_spline(xnew3)



#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.errorbar(pressure_peak_BX[0], gm_counts_peak_BX[0], yerr=gm_counts_peak_BX[1], fmt="o")
#plt.plot(xnew3, ynew3)
#plt.title('k = 4 spline interpolation')
#plt.show()


print str(pfotzer_KMI) + " +- " + str(pfotzer_error_KMI) + ".... #points = " + str(peak_points_KMI)
print str(pfotzer_KNMI) + " +- " + str(pfotzer_error_KNMI) + ".... #points = " + str(peak_points_KNMI)
print str(pfotzer_BX) + " +- " + str(pfotzer_error_BX) + ".... #points = " + str(peak_points_BX)