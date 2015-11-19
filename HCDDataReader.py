# Software versions of known datasets:
# KMI2012 : -1
# KMI2013 : 0
# KMI102014 : 1
# KNMI042015 : 2
# KirunaSystemTest102015 : 3
# BEXUSGSFlightData.txt : 3
# BEXUSDetectorFlightData : 3

##############################################################
# STEPS TO ADD A NEW VERSION OF DATA FILES #
# 1) Add version number to self.__software_versions
# 2) Add an if clause in self.__set_dataset_vars() where you make the dataset vars array with same naming conventions
# as previous versions and in order of how the columns are written to the datafile
# 3) Add an if claus in self.__set_num_skip_lines() where you add how many lines the header takes


import os
import re

class HCDDataReader:

    def __init__(self, dir_or_filename, software_version=3):
        '''
        :param dir_or_filename: This is either the directory (~ symbol not allowed. Type "/home/USERNAME/" instead) of the microcontroller dataset "M_x.txt" or
         the filename for the single file dataset
        :param software_version: Defines how we will read the columns in the datafile
        '''
        self.__software_versions = [-1, 0, 1, 2, 3]
        self.dataset_vars = []

        self.groundstation_data = False
        self.software_version = 0
        self.filename = ""  # filename of single file dataset (for example groundstation)
        self.directory = ""  # directory where microcontroller datafiles are stored
        self.file_names = []  # datafile names fetched by glob
        self.num_skip_lines = 0  # This is the number of lines that the header of the data file take

        self.__dir_or_file_check(dir_or_filename)
        self.set_software_version(software_version)
        self.__set_num_skip_lines()
        self.__findfiles()

        self.__set_dataset_vars()
        self.readout_dict = {idx: key for idx, key in enumerate(self.dataset_vars)}

        self.data = {key: [] for key in self.dataset_vars}

        self.__read_datafiles()


    def __dir_or_file_check(self, dir_or_filename):
        """
        :param dir_or_filename: String that is the path to a file or directory
        :return: sets the directory (if it's a directory) or the filename (if it's just a file)
        """
        if os.path.isdir(dir_or_filename):
            self.groundstation_data = False
            self.directory = dir_or_filename
        elif os.path.isfile(dir_or_filename):
            self.groundstation_data = True
            self.__set_filename(dir_or_filename)
        else:
            print "Input is not an existing directory or filename (case sensitive)."

    def set_software_version(self, software_version):
        """
        :param software_version: an integer that should be in self.software_versions.
        :return: Will determine what variables and which position they are in the datafiles
        """
        if software_version in self.__software_versions:
            self.software_version = software_version
        else:
            print "Software version not recognized. See HCDReader.py for possible versions"

    def __set_num_skip_lines(self):
        """
        :return: Sets the amount of lines the header of the datafiles contain
        """
        if self.groundstation_data:
            self.num_skip_lines = 0
        else:
            if self.software_version == 0:
                self.num_skip_lines = 0
            elif self.software_version == 1:
                self.num_skip_lines = 3
            elif self.software_version == 2:
                self.num_skip_lines = 3
            elif self.software_version == 3:
                self.num_skip_lines = 1

    def __set_filename(self, filename):
        """
        :param filename: filename of the single file dataset (or groundstation dataset, which is 1 file)
        :return:
        """
        if filename[-4:].lower() == ".txt":
            self.filename = filename
        else:
            print "Not a valid extension for filename. Has to be a .txt file"



    def __findfiles(self):
        """
        :return: Will make a list of all the datafiles ordered in ascending order
        """
        if self.groundstation_data:
            self.file_names.append(self.filename)
        else:
            for root, dirs, files in os.walk(self.directory):
                for data_file in files:
                    if data_file[-4:].lower() == ".txt" and data_file[:2].lower() == "m_":
                        self.file_names.append(self.directory + os.sep + data_file)
                if not self.file_names:
                    print "No datafiles found. Datafiles need to be in the format \"M_x.txt\" (case insensitive)"
                else:
                    self.__sort_nicely(self.file_names)

# HUMAN SORTING FUNCTIONS. Example: M_1, M_10, M_11, M_2, M_20 becomes M_1, M_2, M_10, M_11, M_20
###########################################################################################
    def __tryint(self, s):
        try:
            return int(s)
        except:
            return s

    def __alphanum_key(self, s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        return [self.__tryint(c) for c in re.split('([0-9]+)', s)]

    def __sort_nicely(self, l):
        """ Sort the given list in the way that humans expect.
        """
        l.sort(key=self.__alphanum_key)
########################################################################################

    def __set_dataset_vars(self):
        """
        :return: Determines what variables are stored in the specified versions data files
        """
        if self.software_version == 3:
            self.dataset_vars = ["timestamp", "gm1", "gm2", "gm3", "gm4", "1+2", "1+3", "1+4", "2+3", "2+4",
                                   "3+4", "1+2+3", "1+2+4", "1+3+4", "2+3+4", "1+2+3+4", "voltref", "voltp1", "voltp2", "voltp3",
                                   "voltntc", "tempntc", "tempdig",  "press1", "press2", "press3", "hvstate", "pbsstate",
                                   "ethstate", "listenpbs", "sdstate", "looptimer"]
        elif self.software_version == 2:
            self.dataset_vars = ["timestamp", "int", "gm1", "gm2", "gm3", "gm4",  "1+2", "1+3", "1+4", "2+3", "2+4",
                                 "3+4", "1+2+3", "1+2+4", "1+3+4", "2+3+4", "1+2+3+4", "tempdig", "tempntc", "voltntc",
                                 "voltref", "voltp1", "press1", "pbsstate", "current_press_pbs", "mean_press_pbs"]
        elif self.software_version == 1:
            self.dataset_vars = ["timestamp", "int", "gm1", "gm2", "gm3", "gm4", "1+2", "1+3", "1+4", "2+3", "2+4",
                                 "3+4", "1+2+3", "1+2+4", "1+3+4", "2+3+4", "1+2+3+4", "tempdig", "tempntc", "voltntc",
                                 "voltref", "voltp1", "press1"]
        elif self.software_version == 0:
            self.dataset_vars = ["timestamp", "int", "gm1", "gm2", "1+2", "tempdig", "tempntc",  "voltntc", "voltref"]
        elif self.software_version == -1:
            self.dataset_vars = ["gm1", "timestamp"]


    def __read_datafiles(self):
        """
        :return: The opening and reading of the data files happens here.
        """
        for file in self.file_names:
            data = open(file)
            for num_line, line in enumerate(data):
                if num_line > self.num_skip_lines:
                    values = line.split("\t")
                    try:
                        for key in self.readout_dict:
                            data_tag = self.readout_dict[key]
                            data_value = float(values[key])
                            self.data[data_tag].append(data_value)
                    except IndexError:
                        print "Incomplete data line. Skipping to next."
                        print "Happened in file: ", file
                        print "On line: ", num_line
                        self.__data_consistency_check()
                        pass
                    except ValueError:
                        print "Incomplete data line. Skipping to next."
                        print "Happened in file: ", file
                        print "On line: ", num_line
                        self.__data_consistency_check()
                        pass


    def __data_consistency_check(self):
        """
        :return: This will get called when there's a value error (cant convert empty string to float) or index error
         (cant access nonexistent column in read line. These errors happen when a line is incomplete (detector shutdown)
         We will throw the data from the incomplete dataline away. (Should only happen on 1 line (the last one))
        """
        length_dict = {key: len(self.data[key]) for key in self.data}
        minimal_length = 0
        compare_length = 0
        for key in length_dict:
            if minimal_length == 0:
                minimal_length = length_dict[key]
            elif compare_length == 0:
                compare_length = length_dict[key]
            else:
                if minimal_length > compare_length:
                    minimal_length = compare_length
                    compare_length = 0
        for key in length_dict:
            if length_dict[key] > minimal_length:
                self.data[key].pop()


