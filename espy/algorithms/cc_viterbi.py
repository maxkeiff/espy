def xor(bit0,bit1):
    if(bit0==bit1):
        return "0"
    else:
        return "1"
    
def cc_encode(message):
    """Encodes the given message with a rate of 1/2, using the generator polynomials 111 and 110
    
    Args: 
        message (str): a string consisting of 0s and 1s
        
    Returns:
        str: encoded message
    """
    register = ["0","0","0"]
    enc_message = []
    for t in range (0,len(message)):

        register[2]=register[1]
        register[1]=register[0]

        register[0]= message[t]
        state = register[0]+ register[1]
        enc_message.append([])

        enc_message[t] = xor(xor(register[0],register[1]),register[2])+            xor(register[0],register[2])

    return enc_message
 
start_metric = {'zero':0,'one':0, 'two':0,'three':0}
state_machine = {
    #current state, possible branches, branch information
    'zero': {'b1': {'out_b':"11",'prev_st': 'one','input_b':"0"},
             'b2': {'out_b':"00",'prev_st': 'zero','input_b':"0"}},
    'one': {'b1': {'out_b': "01", 'prev_st': 'three', 'input_b':"0"},
             'b2': {'out_b': "10", 'prev_st': 'two', 'input_b':"0"}},
    'two': {'b1': {'out_b': "11", 'prev_st': 'zero', 'input_b':"1"},
             'b2': {'out_b': "00", 'prev_st': 'one', 'input_b':"1"}},
    'three': {'b1': {'out_b': "10", 'prev_st': 'three', 'input_b':"1"},
             'b2': {'out_b': "01", 'prev_st': 'two', 'input_b':"1"}},
 
}
 
def bits_diff_num(num_1,num_2):
    diff=0;
    for i in range(0,len(num_1),1):
        if num_1[i]!=num_2[i]:
            diff+=1
    return diff
 
def cc_decode(rec_message, state_machine, start_metric):
    """Decodes the given message, using the Viterbi algorithm with the given state_machine
    
    Args: 
        rec_message (str): a string consisting of 0s and 1s
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
        for st in state_machine:
            
            prev_st = state_machine[st]['b1']['prev_st']
            first_b_metric = V[(t-1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b1']['out_b'], rec_message[t - 1])
            prev_st = state_machine[st]['b2']['prev_st']
            second_b_metric = V[(t - 1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b2']['out_b'], rec_message[t - 1])
            
            if first_b_metric > second_b_metric:
                V[t][st] = {"metric" : second_b_metric,"branch":'b2'}
            else:
                V[t][st] = {"metric": first_b_metric, "branch": 'b1'}

    smaller = min(V[t][st]["metric"] for st in state_machine)
    #traceback most likely path
    dec_message=[]
    for st in state_machine:
        if V[len(rec_message)-1][st]["metric"] == smaller:
            source_state = st
            for t in range(len(rec_message),0,-1):
                branch = V[t][source_state]["branch"]
                dec_message.append(state_machine[source_state][branch]['input_b'])
                source_state = state_machine[source_state][branch]['prev_st']  
    #reverse dec_message
    dec_message = dec_message [::-1]
    return dec_message

inputs = ("1","0","0","1","1","0","1","0","0","0","1","0","0","0")
rec_message = (cc_encode(inputs))
dec_message = cc_decode(rec_message, state_machine, start_metric)
print(inputs)
print(dec_message)
print(bits_diff_num(inputs, dec_message))
