import numpy as np
from decodanda import Decodanda, generate_synthetic_data
from decodanda.utilities import z_pval



import numpy as np
import matplotlib.pyplot as plt
from decodanda import Decodanda, FakeSession

data = generate_synthetic_data(n_neurons=80, n_trials=100, rateB=0.3, rateA=0.3, keyA='stimulus', keyB='action')
dec = Decodanda(
        data=data,
        conditions={'action': [-1, 1], 'stimulus': [-1, 1]},
        zscore=True,
        verbose=True)
dec.geometrical_analysis()

# We create a synthetic data set where neurons respond to two variables, labeled as
#  - behaviour_letter (taking values A, B)
#  - behaviour_number (taking values 1, 2)
# neural activity is stored under the 'raster' keyword
#
# Through the geometry_analysis() function, here we test
# - the decoding() function
# - the CCGP() function
# - all the dichotomy logic

np.random.seed(0)

conditions = {
    'number': {
        '1': lambda s: s.behaviour_number < 1.5,
        '2': lambda s: s.behaviour_number > 1.5
    },

    'letter': {
        'A': lambda s: s.behaviour_letter == 'A',
        'B': lambda s: s.behaviour_letter == 'B'
    },

    'color': {
        'r': lambda s: s.behaviour_color == 'red',
        'g': lambda s: s.behaviour_color == 'green'
    }
}

# Disentangled representations
s1 = FakeSession(n_neurons=120,
                 ndata=2000,
                 noise_amplitude=0.02,
                 coding_fraction=0.3,
                 rotate=False,
                 symplex=False)

mydec = Decodanda(data=s1,
                  conditions=conditions,
                  verbose=False)


mydec.CCGP(plot=True)

mydec.geometrical_analysis(training_fraction=0.8, nshuffles=20, visualize=True)
plt.suptitle('Disentangled representations')
plt.savefig('./geometry_analysis_disentangled.pdf')

# Entangled representations
s1 = FakeSession(n_neurons=120,
                 ndata=2000,
                 noise_amplitude=0.02,
                 coding_fraction=0.3,
                 rotate=True,
                 symplex=True)

mydec = Decodanda(data=s1,
                  conditions=conditions,
                  verbose=False)

mydec.geometrical_analysis(training_fraction=0.8, nshuffles=20, visualize=True)
plt.suptitle('Entangled representations')
plt.savefig('./geometry_analysis_entangled.pdf')