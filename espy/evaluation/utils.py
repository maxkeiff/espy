import numpy as np


def count_bit_errors(packet):
    return sum(1 for a, b in zip(packet.msg_sent, packet.msg_received) if a != b)


def check_false_positive(packet):
    return packet.payload_valid and packet.payload != packet.payload_received


def check_false_negative(packet):
    return not packet.payload_valid and packet.payload == packet.payload_received


def packet_loss_count(packet_list):
    return len(packet_list) - len(set([packet.packet_id for packet in packet_list]))


def avg_bit_errors(packet_list):
    return sum([count_bit_errors(packet) for packet in packet_list]) / len(packet_list)


def count_positives(packet_list):
    return sum(1 for packet in packet_list if packet.payload_valid)


def count_negatives(packet_list):
    return sum(1 for packet in packet_list if not packet.payload_valid)


def count_false_positives(packet_list):
    return sum(1 for packet in packet_list if check_false_positive(packet))


def count_false_negatives(packet_list):
    return sum(1 for packet in packet_list if check_false_negative(packet))


def analyse_packet_list(packet_list):
    positives = count_positives(packet_list)
    negatives = count_negatives(packet_list)
    false_positives = count_false_positives(packet_list)
    false_negatives = count_false_negatives(packet_list)

    return {
        "positives": positives,
        "negatives": negatives,
        "true_positives": positives - false_positives,
        "true_negatives": negatives - false_negatives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }


def analyse_simulation_results(packet_dict):
    """
    Args:
        dict: some key that will be preserved, value is a packet_list
        
    Returns:
        dict: Same keys, values are dicts of analyse results
    """

    result = {}
    for key, value in packet_dict.items():
        result[key] = analyse_packet_list(value)
    return result


def analyse_3d_simulation_results(packet_array, function):

    result = np.empty((len(packet_array), len(packet_array[0])))

    for list_i, packet_list in enumerate(packet_array):
        for j, packet in enumerate(packet_list):
            result[list_i][j] = function(packet)
    return result
