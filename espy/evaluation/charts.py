import numpy as np
import matplotlib.pyplot as plt


# ber (x-axis) to positives (y-axis) + false positives
# ber (x-axis) to negatives (y-axis) + false negatives


def ber_to_abs(data, xlabel):
    """
    Args:
        dict: values as x axis and dict with keys 
                positives
                negatives
                true_positives
                true_negatives
                false_positives
                false_negatives
    """

    plt.xlabel(xlabel)
    plt.ylabel("packets")
    x_axis = np.array(list(data.keys()))
    dict_list = data.values()

    positives = np.array([d.get("positives") for d in dict_list])
    negatives = np.array([d.get("negatives") for d in dict_list])

    true_positives = [d.get("true_positives") for d in dict_list]
    true_negatives = [d.get("true_negatives") for d in dict_list]
    false_positives = [d.get("false_postives") for d in dict_list]
    false_negatives = [d.get("false_negatives") for d in dict_list]

    plt.plot(x_axis, positives, "r")
    plt.plot(x_axis, negatives, "b")
    plt.plot(x_axis, true_positives, "y")
    plt.plot(x_axis, true_negatives, "o")
    plt.plot(x_axis, false_positives, "g")
    plt.plot(x_axis, false_negatives, "p")
    plt.show()


def two_dimension_heatmap(data, xmin, xmax, ymin, ymax):
    """
    Args: 
        nparray with two dimensions
    """

    # interpolation gaussian
    plt.xlabel("x axis")
    plt.ylabel("y axis")
    image = plt.imshow(
        data,
        cmap="Greens",
        interpolation="none",
        extent=[xmin, xmax, ymax, ymin],
        aspect="auto",
    )

    plt.colorbar(image)
    plt.show()
