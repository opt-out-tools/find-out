import numpy as np
import numpy.lib.recfunctions as rfn
from scipy import sparse
from torch.utils.tensorboard import SummaryWriter
from metal.analysis import lf_summary


def make_Ls_matrix(data, labeling_functions):
    """Returns a labeling function matrix.

    Args:
        data (pandas df) : the text to be labeled.
        labeling_functions (list) : a list of labeling functions to be performed on the text.

    Returns:
        noisy_labels (ndarray) : an nd numpy array of the labels for the text.

    """
    noisy_labels = np.empty((len(data), len(labeling_functions)))

    for i, row in data.iterrows():
        for j, lf in enumerate(labeling_functions):
            noisy_labels[i][j] = lf(row.values[0].lower())
    return noisy_labels


def using_generator_function_make_Ls_matrix(data, generator_labeling_functions):
    """Returns a labeling function matrix calculated using  generator functions.

    Args:
        data (pandas df) : the text to be labeled with.
        labeling_functions (list) : a list of generator labeling functions to be performed on the text.

    Returns:
        noisy_labels (ndarray) : an nd numpy array of the labels for the text.
    """

    names = [get_names(lf("")) for lf in generator_labeling_functions][0]

    noisy_labels = np.empty((len(data), len(names)))

    for i, row in data.iterrows():
        for lf in generator_labeling_functions:
            gen = lf(row.values[0].lower())
        j = 0
        while j < len(names):
            noisy_labels[i][j] = next(gen)[0]
            j += 1

    return noisy_labels, names

def get_names(generator):
    names = []
    j = 0
    while j < 1000:
        try:
            name = next(generator)[1]
            names.append(name)
        except StopIteration:
            break
    return names

def analysis_of_weak_labeling(data, true_labels, labeling_functions, labeling_function_names, generator_labeling_functions):
    """Displays the summary of labeling functions.

    Args:
        data (pandas df) : the text to be labeled with.
        true_labels (pandas series) : the current labels of the data.
        labeling_functions (list) : a list of labeling functions to be performed on the text.
        labeling_function_names (list) : a list of the name of the labeling functions to be performed on the text.
        generator_labeling_functions (list) : a list of labeling functions to be performed on the text.

    Returns:
        Displays a summary of the labeling function's success on the text.
    """
    SummaryWriter()
    labeling_function_matrix = make_Ls_matrix(data, labeling_functions)
    generator_labeling_function_matrix, names = using_generator_function_make_Ls_matrix(data, generator_labeling_functions)
    concat_matrix = np.hstack((labeling_function_matrix, generator_labeling_function_matrix))
    true_labels = np.array(true_labels)
    print(lf_summary(sparse.csr_matrix(concat_matrix), Y=true_labels, lf_names=labeling_function_names + names))


