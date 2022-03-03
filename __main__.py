#!/usr/bin/python3

if __name__ == "__main__" :
    import argparse
#    import spins
#    import thermo
    import numpy as np
    import math
    import ising
#    import hamiltonian

    import matplotlib.pyplot as plot
#    import hamiltonian

    import concurrent.futures

    parser = argparse.ArgumentParser(description = "Plot thermodynamic values" +
                                     " of an Ising system.")
    parser.add_argument("--length", "-l", metavar = "N", default = 10,
                        type = int,
                        help = "Number of positions in the Ising system with" +
                        " periodic boundary conditions.")
    parser.add_argument("--coupling", "-j", metavar = "J", default = -1 *
                        ising.BOLTZMANN_K,
                        type = float, help = "Spin coupling constant.")
    parser.add_argument("--magnet", "-m", metavar = "M", default = 0.1 *
                        ising.BOLTZMANN_K,
                        type = float, help = "Magnetic coupling constant")
    parser.add_argument("--low-temp", metavar = "T",
                        default = 0.1, type = float,
                        help = "Lower temperature in Kelvin")
    parser.add_argument("--high-temp", metavar = "T",
                        default = 298.15, type = float,
                        help = "Higher temperature in Kelvin")
    parser.add_argument("--boltzmann", "-k", metavar = "K",
                        default = ising.BOLTZMANN_K, type = float,
                        help = "Value of the Boltzmann constant to use.")
    parser.add_argument("--points", "-n", metavar = "N",
                        default = 100, type = int,
                        help = "Number of points to use in each graph.")

    args = vars(parser.parse_args())

    exc = concurrent.futures.ThreadPoolExecutor()
    ham = ising.Hamiltonian(args["coupling"], args["magnet"])
    
    temps = np.linspace(args['low_temp'], args["high_temp"], args["points"])
    ens = list(exc.map(lambda t: ising.average_value(ham.energy, ham,
                                                 args["length"],temp = t,
                                                 boltzmann = args["boltzmann"]),
                       temps))
    plot.figure()
    plot.plot(temps, ens, label = "Energy")
    plot.xlabel("Temperature (K)")
    plot.ylabel("Energy")
    plot.legend()
    try :
        endev = list(exc.map(lambda t: math.sqrt(ising.variance(ham.energy, ham,
                                                  args["length"], temp = t,
                                                  boltzmann = args["boltzmann"])
                                   ) / (args["boltzmann"] * t ** 2),
                         temps))
        magdev = list(exc.map(lambda t: math.sqrt(ising.variance(
            lambda sc: sc.magnetization(), ham, args["length"], temp = t,
            boltzmann = args["boltzmann"])) / (args["boltzmann"] * t), temps))
        plot.figure()
        plot.plot(temps, endev, label = "Heat capacity")
        plot.xlabel("Temperature (K)")
        plot.ylabel("Energy per Kelvin")
        plot.legend()
        plot.figure()
        plot.plot(temps, magdev, label = "Magnetic susceptibility")
        plot.xlabel("Temperature (K)")
        plot.ylabel("Energy per Kelvin")
        plot.legend()
    except :
        print("Error on variance")
    exc.shutdown()
    plot.show()
    
