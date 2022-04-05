#!/usr/bin/python3

def main(pass_args = None, test = False) :
    """
Runs the Ising command line program.
    """
    import argparse
    try :
        import spins
        import thermo
        import constants
        import hamiltonian
        import fastcwrapper
    except ImportError :
        from . import spins
        from . import thermo
        from . import constants
        from . import hamiltonian
        from . import fastcwrapper
    import numpy as np
    import math
    import os

    import matplotlib.pyplot as plot

    import concurrent.futures

    # Add command line arguments.
    parser = argparse.ArgumentParser(description = "Plot thermodynamic values" +
                                     " of an Ising system.")
    parser.add_argument("--length", "-l", metavar = "N", default = 10,
                        type = int,
                        help = "Number of positions in the Ising system with" +
                        " periodic boundary conditions.")
    parser.add_argument("--coupling", "-j", metavar = "J", default = -1 *
                        constants.BOLTZMANN_K,
                        type = float, help = "Spin coupling constant.")
    parser.add_argument("--magnet", "-m", metavar = "M", default = 0.1 *
                        constants.BOLTZMANN_K,
                        type = float, help = "Magnetic coupling constant")
    parser.add_argument("--low-temp", metavar = "T",
                        default = 0.1, type = float,
                        help = "Lower temperature in Kelvin")
    parser.add_argument("--high-temp", metavar = "T",
                        default = 298.15, type = float,
                        help = "Higher temperature in Kelvin")
    parser.add_argument("--boltzmann", "-k", metavar = "K",
                        default = constants.BOLTZMANN_K, type = float,
                        help = "Value of the Boltzmann constant to use.")
    parser.add_argument("--points", "-n", metavar = "N",
                        default = 100, type = int,
                        help = "Number of points to use in each graph.")
    parser.add_argument("--python", action="store_true",
                        help = "Use python backend instead of C backend.")
    parser.add_argument("--threads", metavar = "N",
                        default = max(32, 4 + os.cpu_count()), type = int,
                        help = "Number of threads to use.")
    if pass_args == None :
        args = vars(parser.parse_args())
    else :
        args = vars(parser.parse_args(pass_args))

    temps = np.linspace(args['low_temp'], args["high_temp"], args["points"])

    ens, endev, magdev = fastcwrapper.plotvals(hamiltonian.PeriodicHamiltonian(
            args["coupling"], args["magnet"]), args["length"], temps,
                                           threads = args["threads"],
                                       no_c = args["python"])
    plot.figure()
    plot.plot(temps, ens, label = "Energy")
    plot.xlabel("Temperature")
    plot.ylabel("Energy")
    plot.legend()
    plot.figure()
    plot.plot(temps, endev, label = "Heat Capacity")
    plot.xlabel("Temperature")
    plot.ylabel("Energy per Temperature")
    plot.legend()
    plot.figure()
    plot.plot(temps, magdev, label = "Magnetic Susceptibility")
    plot.xlabel("Temperature")
    plot.ylabel("Energy per Temperature")
    plot.legend()
    if not test :
        plot.show()
    else :
        return ens, endev, magdev


if __name__ == "__main__" :
    main()
