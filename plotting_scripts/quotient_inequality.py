import numpy as np

for i in range (10):
    # Create an array of random numbers which are all positive
    f = np.abs(np.random.randn(100)) + 0.0001
    g = np.abs(np.random.randn(100)) + 0.0001

    norm_f = np.sum(f**2) / len(f)
    norm_g = np.sum(g**2) / len(g)

    norm_one_over_f = np.sum(1 / (f**2)) / len(f)
    norm_one_over_g = np.sum(1 / (g**2)) / len(g)

    if norm_f < norm_g:
        good = (norm_one_over_f < norm_one_over_g)
        print(i, norm_f, norm_g, norm_one_over_f, norm_one_over_g, good)

    else:
        good = (norm_one_over_f > norm_one_over_g)
        print(i, norm_f, norm_g, norm_one_over_f, norm_one_over_g, good)
