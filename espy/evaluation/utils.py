import numpy as np


def check_false_positive(packet):
    return packet.payload_valid and packet.payload != packet.payload_received


def check_false_negative(packet):
    return not packet.payload_valid and packet.payload == packet.payload_received


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


def analyse_3d_simulation_results(packet_array, keyword):

    result = np.empty((len(packet_array), len(packet_array[0])))

    for list_i, packet_list in enumerate(packet_array):
        for j, packet in enumerate(packet_list):
            result[list_i][j] = packet.get(keyword)
    return result
