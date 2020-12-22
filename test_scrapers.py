""" Docstring text
"""
__version__ = '0.1'
__author__ = 'David H. Currie'
__copyright__ = 'Copyright (c) 2019 by GeoAnalytic Inc.'
__license__ = 'Proprietary and confidential - Unauthorized copying of this file, via any medium is strictly prohibited'
__email__ = "dcurrie@geoanalytic.com"
__status__ = "Production"

import pickle
import random
from scrapers import gogetcisdata, gogetnicdata, parse_htmlform_files, get_vector_stats

nic_pickle = 'nicfiles.pkl'


def pickle_nic_files():
    """ query the NIC site and store all results in a pickle file for later use """
    t = gogetnicdata()
    pickle.dump(t, open(nic_pickle, 'wb'))
    return len(t)


def load_nic_test():
    x = pickle.load(open(nic_pickle, 'rb'))
    return x


def nic_samples(k=1):
    """ return a random sample (size = k) of the NIC data """
    return random.sample(load_nic_test(), k)


def get_some_stats(k=200):
    """ get a big set of stats for NIC files """
    x = nic_samples(k)
    stats = []
    for sample in x:
        if '_a' in sample[0]:
            print("Skipping {0}".format(sample[0]))
        else:
            print("Processing {0}".format(sample[0]))
            intype = 'e00' if 'e00' in sample[0] else 'zip'
            stats.append(get_vector_stats(sample[1], intype))

    pickle.dump(stats, open('nicstats.pkl', 'wb'))
    return stats
