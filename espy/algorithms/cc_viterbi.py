def encode_message(message, rate=0.5):
    """Encodes a given message using a convolutional encoder with the specified rate
    Args:
        message (str): a string consisting of 0s and 1s
        rate (float): the rate of the encoder, currently available are 0.25, 0.5 and 0.75
    Returns:
        list: a list of strings which represents the encoded message
    """
    message = message + "000"
    if rate == 0.25:
        return cc_encode(message,4)
    elif rate == 0.5:
        return cc_encode(message,3)
    elif rate == 0.75:
        return cc_encode(message,3,True)
    else:
        print("No such rate available.")
        
def decode_message(message, rate=0.5):
    """Decodes a given message using a convolutional decoder with the specified rate
    Args:
        message (list): a message encoded by the function encode_message
        rate (float): the rate of the encoder, currently available are 0.25, 0.5 and 0.75
    Returns:
        list: a list of strings which represents the decoded message
    """
    if rate == 0.25:
        dec_message = cc_decode(message, state_machine_cons_4, start_metric_cons_4)
        return dec_message[0:-3]
    elif rate == 0.5:
        dec_message = cc_decode(message, state_machine, start_metric)
        return dec_message[0:-3]
    elif rate == 0.75:
        dec_message = cc_decode(message, state_machine, start_metric, True)
        return dec_message[0:-3]
    else:
        print("No such rate available")

def xor(bit0,bit1):
    if bit0 == bit1:
        return "0"
    else:
        return "1"
    
def cc_encode(message, constraint_length = 3, punctured = False):
    """Encodes the given message using convolutional coding (by default with a rate of 1/2, using the generator polynomials 111 and 101)
    
    Args: 
        message (str): a string consisting of 0s and 1s
        constraint_length (int): number of bits used to calculate parity bits, default is 3 for a rate of 1/2
        punctured (bool): whether puncturing is used or not (only available for rate constraint_length 3)
        
    Returns:
        list: encoded message
    """
    #code rate 1/2 using 3[5,7]
    enc_message =[]
    if constraint_length == 3:
        register = ["0","0","0"]
        
        punct_count = 0
        for t in range(0,len(message)):
            #filling register
            register[2]=register[1]
            register[1]=register[0]

            register[0]= message[t]
            
            #applying generator polynomials 111 and 101
            if punctured == False:
                enc_message.append(xor(xor(register[0],register[1]),register[2])+xor(register[0],register[2]))
            else:
                #puncturing code, using the puncturing matrix consisting of the rows (110) and (101), thus resulting in rate 3/4
                if punct_count == 0:
                    enc_message.append(xor(xor(register[0],register[1]),register[2])+xor(register[0],register[2]))
                    punct_count = (punct_count+1)%3 
                elif punct_count == 1:
                    enc_message.append(xor(xor(register[0],register[1]),register[2]))
                    punct_count = (punct_count+1)%3
                else:
                    enc_message.append(xor(register[0],register[2]))
                    punct_count = (punct_count+1)%3
                    
    #code rate 1/4 using 
    elif constraint_length == 4:
        register = ["0","0","0","0"]
        for t in range(0,len(message)):
            #filling register
            register[3]=register[2]
            register[2]=register[1]
            register[1]=register[0]

            register[0]= message[t]
            
            #applying generator polynomials 1001,1111,1110,1011
            enc_bit=""
            enc_bit += xor(register[0],register[3])
            enc_bit += xor(xor(xor(register[0],register[1]),register[2]),register[3])
            enc_bit += xor(xor(register[0],register[1]),register[2])
            enc_bit += xor(xor(register[0],register[2]),register[3])
            enc_message.append(enc_bit)
    
    return enc_message
 
start_metric = {'A':0,'B':1, 'C':1,'D':1}
state_machine = {
    #current state, possible branches, branch information
    'A': {'b1': {'out_b':"11",'prev_st': 'B','input_b':"0"},
             'b2': {'out_b':"00",'prev_st': 'A','input_b':"0"}},
    'B': {'b1': {'out_b': "01", 'prev_st': 'D', 'input_b':"0"},
             'b2': {'out_b': "10", 'prev_st': 'C', 'input_b':"0"}},
    'C': {'b1': {'out_b': "11", 'prev_st': 'A', 'input_b':"1"},
             'b2': {'out_b': "00", 'prev_st': 'B', 'input_b':"1"}},
    'D': {'b1': {'out_b': "10", 'prev_st': 'D', 'input_b':"1"},
             'b2': {'out_b': "01", 'prev_st': 'C', 'input_b':"1"}},
 
}


start_metric_cons_4 = {'A':0,'B':1, 'C':1,'D':1, 'E':1, 'F':1, 'G':1, 'H':1}
state_machine_cons_4 = {
    #current state, possible branches, branch information
    'A': {'b1': {'out_b':"1101",'prev_st': 'H','input_b':"0"},
             'b2': {'out_b':"0000",'prev_st': 'A','input_b':"0"}},
    'B': {'b1': {'out_b': "1111", 'prev_st': 'A', 'input_b':"1"},
             'b2': {'out_b': "0010", 'prev_st': 'H', 'input_b':"1"}},
    'C': {'b1': {'out_b': "1001", 'prev_st': 'B', 'input_b':"1"},
             'b2': {'out_b': "0100", 'prev_st': 'F', 'input_b':"1"}},
    'D': {'b1': {'out_b': "0011", 'prev_st': 'D', 'input_b':"1"},
             'b2': {'out_b': "1110", 'prev_st': 'C', 'input_b':"1"}},
    'E': {'b1': {'out_b':"0110",'prev_st': 'B','input_b':"0"},
             'b2': {'out_b':"1011",'prev_st': 'F','input_b':"0"}},
    'F': {'b1': {'out_b': "1000", 'prev_st': 'E', 'input_b':"1"},
             'b2': {'out_b': "0101", 'prev_st': 'G', 'input_b':"1"}},
    'G': {'b1': {'out_b': "0001", 'prev_st': 'C', 'input_b':"0"},
             'b2': {'out_b': "1100", 'prev_st': 'D', 'input_b':"0"}},
    'H': {'b1': {'out_b': "1010", 'prev_st': 'G', 'input_b':"0"},
             'b2': {'out_b': "0111", 'prev_st': 'E', 'input_b':"0"}},
 
}
 
def bits_diff_num(num_1,num_2):
    diff=0;
    for i in range(0,len(num_1),1):
        if num_1[i]!=num_2[i]:
            diff+=1
    return diff
 
def cc_decode(rec_message, state_machine, start_metric, punctured = False):
    """Decodes the given message, using the Viterbi algorithm with the given state_machine
    
    Args: 
        rec_message (list): a list of strings of 0s and 1s (usually generated by cc_encode)
        state_machine (set): a set of all possible transient states while encoding a message
        start_metric (set): a set of the startin probabilities for each state
        
    Returns:
        str: decoded message
    """

        
    V = [{}]
    for st in state_machine:
        #inserting start metric
        V[0][st] = {"metric": start_metric[st]}     

    for t in range(1, len(rec_message)+1):
        V.append({})
        punct_count = 0
        for st in state_machine:
            prev_st = state_machine[st]['b1']['prev_st']
            if punctured == False or punct_count == 0:
                first_b_metric = V[(t-1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b1']['out_b'], rec_message[t - 1])
            elif punct_count == 1:
                first_b_metric = V[(t-1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b1']['out_b'][0], rec_message[t - 1][0])
            elif punct_count == 2:
                first_b_metric = V[(t-1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b1']['out_b'][1], rec_message[t - 1][1])
            prev_st = state_machine[st]['b2']['prev_st']
            second_b_metric = V[(t - 1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b2']['out_b'], rec_message[t - 1])
            if punctured == False or punct_count == 0:
                second_b_metric = V[(t - 1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b2']['out_b'], rec_message[t - 1])
            elif punct_count == 1:
                second_b_metric = V[(t - 1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b2']['out_b'][0], rec_message[t - 1][0])
            elif punct_count == 2:
                second_b_metric = V[(t - 1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b2']['out_b'][1], rec_message[t - 1][1])
            
            punct_count = (punct_count+1)%3
            
            if first_b_metric > second_b_metric:
                V[t][st] = {"metric" : second_b_metric,"branch":'b2'}
            else:
                V[t][st] = {"metric": first_b_metric, "branch": 'b1'}
                
    min_metric = min(V[t][st]["metric"] for st in state_machine)
    #traceback most likely path
    dec_message=[]
    for st in state_machine:
        if V[len(rec_message)-1][st]["metric"] == min_metric:
            source_state = st
            for t in range(len(rec_message),0,-1):
                branch = V[t][source_state]["branch"]
                dec_message.append(state_machine[source_state][branch]['input_b'])
                source_state = state_machine[source_state][branch]['prev_st']  
    #reverse dec_message
    dec_message = dec_message [::-1]
    
    return dec_message
