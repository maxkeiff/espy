
import numpy
from channel_noise_simulator import channel_noise_simulator

cns = channel_noise_simulator()
example_data = ""
sample_size = 20000
for i in range(sample_size):
    example_data += "0"

error_density_multiplier = 2 #Higher density means smaler but more errors
x1 = 0;
x2 = 0;
count = 1000

enter_error_rate=0.01;
leave_error_rate=0.05;

for i in range(count):
    error_burst1=cns.randomise_bits_burst_string(example_data, enter_error_rate                          ,1-(leave_error_rate))#chance of 1% to start and 1%to end burst
    error_burst2=cns.randomise_bits_burst_string(example_data, enter_error_rate*error_density_multiplier ,1-(leave_error_rate*error_density_multiplier))
    x1+=error_burst1.count('1')
    x2+=error_burst2.count('1')

print(x1/count/sample_size)
print(x2/count/sample_size)

# use Line 16+17 to simulate different lengths of bursterrors while keeping the distribution close to equal.
# This code is used to verify the different distributions. Variation comes from the possibility, that a burst is cut short at the
# end of the message. (bigger samplesize and shorter bursterrors yield better results.)
