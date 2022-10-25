import numpy as np

def read_file(filename):
    '''Reads the SeaDarQ binary file and outputs as a numpy 3d array, with dimensions: '''
    header_num = 512
    metadata_num = 112
    range_num = 1024
    azimuth_num = 4096

    def frame_count(az_vals):
        frame_counter = 1
        for i in range(1, len(az_vals)):
            if az_vals[i] < az_vals[i-1]:
                frame_counter +=1

        return frame_counter


    def create_backscatter_matrix(range_num, azimuth_num, M_cut, az_vals, num_rows_of_M, num_frames):
        B = np.empty((range_num, azimuth_num, num_frames))
        B[:] = np.nan

        frame_indx = 0
        frame_check = 0
        for n in range(int(num_rows_of_M)):
            if az_vals[n] < frame_check:
                frame_indx += 1
            B[:, az_vals[n], frame_indx] = M_cut[n, :]
            frame_check = az_vals[n]

        return B


    def open_binary_file(filename):
        try:
            array1d = np.memmap(filename, dtype='int16', mode='r', offset=header_num*2)
        except IOError:
            print('Error while opening file: ' + filename)

        return array1d


    array1d = open_binary_file(filename)

    num_rows_of_M = np.divide(np.shape(array1d)[0], (metadata_num + range_num))
    M = np.reshape(array1d, (int(num_rows_of_M), (metadata_num + range_num)))

    # Extract azimuth values
    az_vals = M[:, 22]

    # Cut out metadata
    M_cut = np.delete(M, np.s_[0:metadata_num], 1).copy()

    # Determine how many frames there are
    num_frames = frame_count(az_vals)

    B = create_backscatter_matrix(range_num, azimuth_num, M_cut, az_vals, num_rows_of_M, num_frames)

    return B


def test_func():
    print('Yes, test_func is working!')
