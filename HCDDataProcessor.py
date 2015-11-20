import math
import numpy as np
import matplotlib.pyplot as plt

class HCDDataProcessor:

    def __init__(self):
        self.pressure_sensor_deviation = 0.5  # Deviation of the NPA 500B Pressure Sensor used in the experiments
        self.peak_boundary_xmin = None
        self.peak_boundary_xmax = None

    def remove_peaks(self, data):
        """
        :param data: HCDDataReader.data
        :return: Removes all the datapoints where the pressure sensors had a very weird peak
        """
        indices_to_remove = sorted(list(set(self.find_peaks(data))))  #set removes duplicates, list defines an order, sorted gives ascending order
        num_deleted = 0
        for index in indices_to_remove:
            for key in data:
                del data[key][index - num_deleted]
            num_deleted += 1  # We need to shift every index in our "to-delete list" because we are removing elements
        return data

    def find_peaks(self, data):
        """
        :param data: HCDDataReader.data
        :return: List with indices of the datapoints where one or more pressure sensors had a weird peak (delta > 5 or press < -5 (see begin/end KMI data))
        """
        indices_remove_datapoints = []
        pressure_difference_max = 5
        pressure_min = -5
        try:
            if data["press1"]:
                for i, pressure in enumerate(data["press1"]):
                    if i > 0:
                        if abs(pressure - data["press1"][i-1]) > pressure_difference_max or pressure <= pressure_min:
                            indices_remove_datapoints.append(i)
        except KeyError:
            pass
        try:
            if data["press2"]:
                for i, pressure in enumerate(data["press2"]):
                    if i > 0:
                        if abs(pressure - data["press2"][i-1]) > pressure_difference_max or pressure <= pressure_min:
                            indices_remove_datapoints.append(i)
        except KeyError:
            pass
        try:
            if data["press3"]:
                for i, pressure in enumerate(data["press3"]):
                    if i > 0:
                        if abs(pressure - data["press3"][i-1]) > pressure_difference_max or pressure <= pressure_min:
                            indices_remove_datapoints.append(i)
        except KeyError:
            pass
        return indices_remove_datapoints

    def average_counts_over_pressure(self, counts_to_average, pressure_data, binsize=2):
        """
        :param counts_to_average: The array with GM counts that we want to put in bins and average out
        :param pressure_data: The array with pressure data that we want to use as our bins
        :param binsize: defines the width of the pressure bins
        :return: array with the average counts in every bin and array with the poisson error of every average
        """
        counts_average = []
        counts_error = []
        counts_in_bins = []

        max_pressure = max(pressure_data)
        min_pressure = min(pressure_data)
        delta_pressure = abs(max_pressure - min_pressure)

        num_bins = int(math.ceil(delta_pressure / binsize))


        for bin in xrange(num_bins):
            begin_pressurebin = float(max_pressure - bin * binsize)
            end_pressurebin = float(begin_pressurebin - binsize)
            count_average = 0
            num_datapoints_in_bin = 0
            num_counts_in_bin = 0

            for i, pressure in enumerate(pressure_data):
                if end_pressurebin < pressure <= begin_pressurebin:
                    num_datapoints_in_bin += 1
                    num_counts_in_bin += counts_to_average[i]
                    count_average += counts_to_average[i]
            if num_datapoints_in_bin > 0:
                count_average /= num_datapoints_in_bin
                counts_average.append(count_average)
                counts_error.append(math.sqrt(count_average))
            counts_in_bins.append(num_counts_in_bin)
        return np.array(counts_average), np.array(counts_error), np.array(counts_in_bins)

    def pressurebin_centers(self, pressure_data, binsize=2):
        pressures_average = []
        pressures_error = []

        max_pressure = max(pressure_data)
        min_pressure = min(pressure_data)
        delta_pressure = abs(max_pressure - min_pressure)

        num_bins = int(math.ceil(delta_pressure / binsize))

        for bin in xrange(num_bins):
            begin_pressurebin = float(max_pressure - bin * binsize)
            end_pressurebin = float(begin_pressurebin - binsize)
            pressure_average = 0
            pressure_error = 0
            num_datapoints_in_bin = 0
            pressures_in_bin = []

            for i, pressure in enumerate(pressure_data):
                if end_pressurebin < pressure <= begin_pressurebin:
                    num_datapoints_in_bin += 1
                    pressure_average += pressure
                    pressures_in_bin.append(pressure)
            if num_datapoints_in_bin > 0:
                pressure_average /= num_datapoints_in_bin
                pressures_average.append(pressure_average)
                if num_datapoints_in_bin > 1:
                    for pressure_val in pressures_in_bin:
                        pressure_error += (pressure_val - pressure_average) ** 2
                    pressure_error *= 1 / (num_datapoints_in_bin * (num_datapoints_in_bin - 1))
                    pressure_error **= 1/2
                else:
                    pressure_error = self.pressure_sensor_deviation
                pressures_error.append(pressure_error)


        return np.array(pressures_average), np.array(pressures_error)


    def datacut_based_on_statedata(self, data_to_cut, state_data, cut_state=0):
        """
        :param data_to_cut: Array with data where we want to extract datapoints when a specific state has been met
        :param state_data: Array with the state data (can be High Voltage, SD, Ethernet, etc. )
        :param cut_state: Defines what the state needs to be to initiate a cut
        :return: An array that is a subset of the start array in which all datapoints that didn't meet the state requirement are removed
        """
        if len(data_to_cut) != len(state_data):
            print "DATA TO CUT AND STATE DATA DONT HAVE SAME LENGTH !"
            print len(data_to_cut)
            print len(state_data)
            return None
        else:
            cut_data = []
            for i, datapoint in enumerate(data_to_cut):
                if state_data[i] == cut_state:
                    cut_data.append(datapoint)
            return np.array(cut_data)

    def weighted_average(self, average_data, error_data):
        """
        :param average_data: A list with all the average arrays that we want to make a weighted average of [average1, average2, ... ]
        :param error_data: A list with all the error arrays that correspond with our averages [error1, error2, ...]
        :return: An array with the weighted averages and an array with the deviations on these weighted errors
        """
        if self.lengths_are_ok(average_data):
            if self.lengths_are_ok(error_data):
                if len(average_data[0]) == len(error_data[0]):
                    weighted_averages = []
                    weighted_errors = []

                    for i in xrange(len(average_data[0])):
                        weighted_average_numerator = 0
                        weighted_average_denominator = 0
                        weighted_error_denominator = 0
                        for j, average_array in enumerate(average_data):
                                if average_array[i] != 0.0 and error_data[j][i] != 0.0:
                                    weighted_average_numerator += (average_array[i] / (error_data[j][i] ** 2))
                                    weighted_average_denominator += (1 / (error_data[j][i] ** 2))
                                    weighted_error_denominator += 1 / (error_data[j][i] ** 2)
                        if weighted_average_denominator != 0.0 and weighted_error_denominator != 0.0:
                            weighted_averages.append(weighted_average_numerator / weighted_average_denominator)
                            weighted_errors.append(math.sqrt(1 / weighted_error_denominator))
                        else:
                            weighted_averages.append(0)
                            weighted_errors.append(0)
                    return np.array(weighted_averages), np.array(weighted_errors)
                else:
                    print "Lengths of error arrays and average arrays aren't the same !"
            else:
                print "Lengths of error arrays aren't the same !"
        else:
            print "Lengths of average arrays aren't the same !"

    def lengths_are_ok(self, multiple_arrays):
        """
        :param multiple_arrays: A list of arrays [array1, array2, ... ]
        :return: Boolean that tells us if all the arrays in the list have the same length
        """
        array_lengths = []
        lengths_ok = True
        for array in multiple_arrays:
            array_lengths.append(len(array))
        for length in array_lengths:
            if array_lengths[0] != length:
                lengths_ok = False
        return lengths_ok


    def set_peak_boundaries(self, xmin=None, xmax=None, x=[], y=[]):
        if xmin == None or xmax == None:
            if len(x) == 0 and len(y) == 0:
                print "If no xmin or xmax are defined, pass x and y vectors to the function so that appropriate boundaries can be chosen from a plot"
            else:
                fig = plt.figure()
                plt.plot(x, y, "o")
                plt.title('Click on the boundaries of the desired peak. Close plot after.')

                peak_boundaries = []

                def onclick(event):
                    ix = event.xdata
                    print 'x = %f' % ix

                    peak_boundaries.append(ix)

                    if len(peak_boundaries) == 2:
                        fig.canvas.mpl_disconnect(cid)

                cid = fig.canvas.mpl_connect('button_press_event', onclick)

                plt.show()

                self.peak_boundary_xmin = min(peak_boundaries)
                self.peak_boundary_xmax = max(peak_boundaries)

                print "Chosen boundaries: xmin = %f, xmax = %f" % (self.peak_boundary_xmin, self.peak_boundary_xmax)
                print "Save these boundaries for future use so that you don't need to click on the plot anymore."
        else:
            if xmin == xmax:
                print "Boundaries have same value ! Pass different boundaries"
            else:
                self.peak_boundary_xmin = min([xmin, xmax])
                self.peak_boundary_xmax = max([xmin, xmax])
        return [self.peak_boundary_xmin, self.peak_boundary_xmax]

    def extract_peak(self, x, y):
        if self.peak_boundary_xmin == None or self.peak_boundary_xmax == None:
            print "Define the peak boundaries first !"
        else:
            peak_x = []
            peak_x_errors = []
            peak_y = []
            peak_y_errors = []

            for i, element in enumerate(x[0]):
                if self.peak_boundary_xmin <= element <= self.peak_boundary_xmax:
                    peak_x.append(element)
                    peak_x_errors.append(x[1][i])
                    peak_y.append(y[0][i])
                    peak_y_errors.append(y[1][i])

            return [peak_x, peak_x_errors], [peak_y, peak_y_errors]