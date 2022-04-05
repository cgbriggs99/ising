#!/usr/bin/python3

def main() :
    import argparse
    try :
        import spins
        import thermo
        import ising
        import hamiltonian
    except ImportError :
        from . import spins
        from . import thermo
        from . import ising
        from . import hamiltonian
    import numpy as np
    import math

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
    parser.add_argument("--python", action="store_true",
                        help = "Use python backend instead of C backend.")

    args = vars(parser.parse_args())


    # Check if using the C backend.
    use_c = not args["python"]
    temps = np.linspace(args['low_temp'], args["high_temp"], args["points"])
    if not args["python"] :
        import os
        try :
            import src.fastc
            use_c = True
        except ImportError :
            try :
                from . import src
                from .src import fastc
                use_c = True
            except ImportError :
                print("Could not find ising.src.fastc")
                use_c = False
    if args["python"] or not use_c :
        # Open up a thread pool. If it's going to run in Python,
        # we might as well try to make it go faster.
        exc = concurrent.futures.ThreadPoolExecutor()
        ham = hamiltonian.Hamiltonian(args["coupling"], args["magnet"])
        ens = list(exc.map(lambda t: thermo.ThermoStrategy.getsingleton().
                           average(ham.energy, ham,
                                                 args["length"],temp = t,
                                                 boltzmann = args["boltzmann"]),
                           temps))
        # Plot.
        plot.figure()
        plot.plot(temps, ens, label = "Energy")
        plot.xlabel("Temperature")
        plot.ylabel("Energy")
        plot.legend()
        # Rinse and repeat.
        endev = list(exc.map(lambda t: math.sqrt(thermo.ThermoStrategy.
                                                 getsingleton().variance(
                                                    ham.energy, ham,
                                                      args["length"], temp = t,
                                                      boltzmann = args["boltzmann"])
                                   ) / (args["boltzmann"] * t ** 2),
                         temps))
        magdev = list(exc.map(lambda t: math.sqrt(thermo.ThermoStrategy.
                                                  getsingleton().variance(
            lambda sc: sc.magnetization(), ham, args["length"], temp = t,
            boltzmann = args["boltzmann"])) / (args["boltzmann"] * t), temps))
        plot.figure()
        plot.plot(temps, endev, label = "Heat capacity")
        plot.xlabel("Temperature")
        plot.ylabel("Energy per Temperature")
        plot.legend()
        plot.figure()
        plot.plot(temps, magdev, label = "Magnetic susceptibility")
        plot.xlabel("Temperature")
        plot.ylabel("Energy per Temperature")
        plot.legend()
        # Don't forget to shutdown the threads.
        exc.shutdown()
        plot.show()
    else :
        # Use the C function, which is also threaded.
        ens, endev, magdev = src.fastc.plot_vals(args["length"],
                                                  args["coupling"],
                                                  args["magnet"],
                                                  list(temps),
                                                  args["boltzmann"],
                                                  min(32, os.cpu_count() + 4))
        # Plot.
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
        plot.show()


if __name__ == "__main__" :
    main()
