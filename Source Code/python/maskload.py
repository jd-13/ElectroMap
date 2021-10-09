import numpy as np

def maskload(filename):
    """
    function for applying loaded map (generated automatically from MatLab)
    Chris O'Shea and Ting Yue Yu, University of Birmingham
    Maintained by Chris O'Shea - Email CXO531@bham.ac.uk for any queries

    Python diff:
        startRow and endRow parameters have been removed as they aren't used.
    """

    # Open the text file.
    with open(filename, "r") as fileID:

        # Read columns of data according to the format.
        # This call is based on the structure of the file used to generate this
        # code. If an error occurs for a different file, try regenerating the code
        # from the Import Tool.
        formatSpec = ["float"] * 1612
        dataArray = np.loadtxt(fileID, dtype={"format": formatSpec}, delimiter=",")

    # Post processing for unimportable data.
    # No unimportable data rules were applied during the import, so no post
    # processing code is included. To generate code which works for
    # unimportable data, select unimportable cells in a file and regenerate the
    # script.

    # Create output variable
    ggg = np.array(dataArray)

    # get rid of NaNs
    ggg = ggg[~np.isnan(ggg)]
