'''data.py
Reads CSV files, stores data, access/filter data by variable name
Adaobi Nebuwa
CS 251 Data Analysis and Visualization
Spring 2022
'''

import csv
import numpy as np


class Data:

    #data types
    dataTypes = ['string','enum','numeric','date']

    def __init__(self, filepath=None, headers=None, data=None, header2col=None, dataDict=None, dataFields=None):
        #print("This is the data constructor")
        '''Data object constructor

        Parameters:
        -----------
        filepath: str or None. Path to data .csv file
        headers: Python list of strings or None. List of strings that explain the name of each
            column of data.
        data: ndarray or None. shape=(N, M).
            N is the number of data samples (rows) in the dataset and M is the number of variables
            (cols) in the dataset.
            2D numpy array of the dataset's values, all formatted as floats.
        header2col: Python dictionary or None.
                Maps header (var str name) to column index (int).
                Example: "sepal_length" -> 0
        '''
        
        #filepath: str or None. Path to data .csv file
        self.filepath = filepath

        #headers: Python list of strings or None. List of strings that explain the name of each column of data.
        if headers != None:
            self.headers = headers
        else:
            self.headers = []

        #data: ndarray or None. shape=(N, M).
        #N is the number of data samples (rows) in the dataset and M is the number of variables
        #cols) in the dataset.
        #2D numpy array of the dataset's values, all formatted as floats.
        try:
            if data == None:
                self.data = []
        except:
            self.data = data


        #dictonary used to store all data
        if dataDict != None:
            self.dataDict = dataDict
        else:
            self.dataDict = {}


        #header2col: Python dictionary or None.
        #Maps header (var str name) to column index (int).
        #Example: "sepal_length" -> 0
        if header2col != None:
            self.header2col = header2col
        else:
            self.header2col = {}


        #Holds dictionary of all the data fields in the data
        #key = headers
        #value = data type
        if dataFields != None:
            self.dataFields = dataFields
        else:
            self.dataFields = {}


        #If `filepath` isn't None, call the `read` method.
        if self.filepath != None:
            self.read(filepath=self.filepath)

        

    def read(self, filepath):
        '''Read in the .csv file `filepath` in 2D tabular format. Convert to numpy ndarray called
        `self.data` at the end (think of this as 2D array or table).

        Format of `self.data`:
            Rows should correspond to i-th data sample.
            Cols should correspond to j-th variable / feature.

        Parameters:
        -----------
        filepath: str or None. Path to data .csv file
        '''
        
        self.filepath = filepath

        with open(filepath,"r") as csv_file:
            reader = csv.reader(csv_file, delimiter = ',')

            #remove white spaces spaces in data
            data = [[x.strip() for x in row] for row in reader]

            #convert data to a numpy array
            self.data = np.array(data)

            #pick out numeric data only
            arr_indx = np.where(self.data[1,:] == 'numeric')

            #change arr_indx from 2D to 1D
            arr_indx = np.array(arr_indx).flatten()

            #ensure we have only numeric headers
            self.headers = self.data[0,arr_indx].tolist()

            #create empy list for header indexes
            header_indx = []

            #append length of arr_inx to header_indx
            for i in range(len(arr_indx)):
                header_indx.append(i)

            #zip header_indx with self.headers to form dictionary of header2col
            d1 = zip(self.headers,header_indx)
            self.header2col = dict(d1)

            #have self.data display only the data without headers and datatypes
            self.data = self.data[2:,arr_indx]

            #convert self.data to type float
            self.data = self.data.astype('float64')

    def __str__(self):
        '''toString method

        Returns:
        -----------
        str. A nicely formatted string representation of the data in this Data object.
            Only show, at most, the 1st 5 rows of data
            See the test code for an example output.
        '''

        # usign python join method to create a nicely formatted to string 
        header = "  ".join(str(header) for header in self.headers)
        rows = "\n".join([' '.join(['{:5}'.format(item) for item in row]) for row in self.data[0:5]])
        column_size = len(self.data[0])
        row_size = len(self.data)

        return f'-------------------------------\n{self.filepath} {row_size}x{column_size} \nHeaders: \n{header}\n-------------------------------\nShowing first 5/{row_size} rows.\n{rows}\n-------------------------------'
        


    def get_headers(self):
        '''Get method for headers

        Returns:
        -----------
        Python list of str.
       '''
        return self.headers
        

    def get_mappings(self):
        '''Get method for mapping between variable name and column index

        Returns:
        -----------
        Python dictionary. str -> int
        '''
        return self.header2col

    def get_num_dims(self):
        '''Get method for number of dimensions in each data sample

        Returns:
        -----------
        int. Number of dimensions in each data sample. Same thing as number of variables.
        '''
        return len(self.headers)
        

    def get_num_samples(self):
        '''Get method for number of data points (samples) in the dataset

        Returns:
        -----------
        int. Number of data samples in dataset.
        '''
        return self.data.shape[0]

    def get_sample(self, rowInd):
        '''Gets the data sample at index `rowInd` (the `rowInd`-th sample)

        Returns:
        -----------
        ndarray. shape=(num_vars,) The data sample at index `rowInd`
        '''
        return self.data[rowInd]

    def get_header_indices(self, headers):
        '''Gets the variable (column) indices of the str variable names in `headers`.

        Parameters:
        -----------
        headers: Python list of str. Header names to take from self.data

        Returns:
        -----------
        Python list of nonnegative ints. shape=len(headers). The indices of the headers in `headers`
            list.
        '''
        headers_indicies = []

        for i in range(len(self.headers)):
            if self.headers[i] in headers:
                headers_indicies.append(i)
        return headers_indicies

    def get_all_data(self):
        '''Gets a copy of the entire dataset

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(num_data_samps, num_vars). A copy of the entire dataset.
            NOTE: This should be a COPY, not the data stored here itself.
            This can be accomplished with numpy's copy function.
        '''
        data_copy = np.copy(self.data)
        return data_copy

    def head(self):
        '''Return the 1st five data samples (all variables)

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(5, num_vars). 1st five data samples.
        '''
        return (self.data[:5])


    def tail(self):
        '''Return the last five data samples (all variables)

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(5, num_vars). Last five data samples.
        '''
        return (self.data[-5:])

    def limit_samples(self, start_row, end_row):
        '''Update the data so that this `Data` object only stores samples in the contiguous range:
            `start_row` (inclusive), end_row (exclusive)
        Samples outside the specified range are no longer stored.

        (Week 2)

        '''
        newDataArray = self.data[start_row:end_row][:]
        self.data = newDataArray

    def select_data(self, headers, rows=[]):
        '''Return data samples corresponding to the variable names in `headers`.
        If `rows` is empty, return all samples, otherwise return samples at the indices specified
        by the `rows` list.

        (Week 2)

        For example, if self.headers = ['a', 'b', 'c'] and we pass in header = 'b', we return
        column #2 of self.data. If rows is not [] (say =[0, 2, 5]), then we do the same thing,
        but only return rows 0, 2, and 5 of column #2.

        Parameters:
        -----------
            headers: Python list of str. Header names to take from self.data
            rows: Python list of int. Indices of subset of data samples to select.
                Empty list [] means take all rows

        Returns:
        -----------
        ndarray. shape=(num_data_samps, len(headers)) if rows=[]
                 shape=(len(rows), len(headers)) otherwise
            Subset of data from the variables `headers` that have row indices `rows`.

        Hint: For selecting a subset of rows from the data ndarray, check out np.ix_
        '''
        columns = []

        #print(self.headers)
        for i in headers:
            columns.append(self.headers.index(i))

        if rows == []:
            return self.data[:,columns]
        else:
            return self.data[np.ix_(rows, columns)]