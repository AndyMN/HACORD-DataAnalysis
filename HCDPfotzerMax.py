from HCDDataReader import HCDDataReader
from HCDDataProcessor import HCDDataProcessor
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

pressure_binsize = 0.5

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

#####################################################################################################################
peak_boundaries = KMI_processor.set_peak_boundaries(xmin=1.853304, xmax=12.565059)
#peak_boundaries = KMI_processor.set_peak_boundaries(x=pressures_KMI_average, y=gm_KMI_weighted_average)
pressure_peak, gm_counts_peak = KMI_processor.extract_peak([pressures_KMI_average, pressures_KMI_error], [gm_KMI_weighted_average, gm_KMI_weighted_error])
weight = []
for error in gm_counts_peak[1]:
    weight.append(1/error)

sorted_x, sorted_y, sorted_weight = (list(x) for x in zip(*sorted(zip(pressure_peak[0], gm_counts_peak[0], weight))))

basic_spline = interpolate.UnivariateSpline(sorted_x, sorted_y, w=sorted_weight, s=1, k=4)
derivative_spline = basic_spline.derivative(1)

xnew = np.arange(min(pressure_peak[0]), max(pressure_peak[0]), 0.01)
ynew_der = derivative_spline(xnew)
ynew = basic_spline(xnew)

roots = derivative_spline.roots()
print roots
coefs = derivative_spline.get_coeffs()
print coefs
knots = derivative_spline.get_knots()
print knots

average_count = np.average(gm_counts_peak[0])
SStot = 0
for count in gm_counts_peak[0]:
    SStot += (count - average_count) ** 2
SSres = basic_spline.get_residual()
Rsquared = 1 - SSres / SStot
print Rsquared




fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.errorbar(pressure_peak[0], gm_counts_peak[0], yerr=gm_counts_peak[1], fmt="o")
#plt.plot(xnew, ynew_der)
plt.plot(xnew, ynew)
plt.title('Quadratic-spline interpolation')
plt.show()

