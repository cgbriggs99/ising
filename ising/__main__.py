#!/usr/bin/python3

"""
Runner for the Ising program.
"""
import os
import sys
import argparse

try:
    import thermo
    import constants
    import hamiltonian
    import fastcwrapper
    import montecarlo
except ImportError:
    from . import thermo
    from . import constants
    from . import hamiltonian
    from . import fastcwrapper
    from . import montecarlo
import numpy as np
import matplotlib.pyplot as plot


def main(pass_args=None, test=False):
    """
Runs the Ising command line program.
    """

    # Add command line arguments.
    parser = argparse.ArgumentParser(
        description="Plot thermodynamic values" + " of an Ising system."
    )
    parser.add_argument(
        "--length",
        "-l",
        metavar="N",
        default=10,
        type=int,
        help="Number of positions in the Ising system with"
        + " periodic boundary conditions.",
    )
    parser.add_argument(
        "--coupling",
        "-j",
        metavar="J",
        default=-1 * constants.BOLTZMANN_K,
        type=float,
        help="Spin coupling constant.",
    )
    parser.add_argument(
        "--magnet",
        "-m",
        metavar="M",
        default=0.1 * constants.BOLTZMANN_K,
        type=float,
        help="Magnetic coupling constant",
    )
    parser.add_argument(
        "--low-temp",
        metavar="T",
        default=0.1,
        type=float,
        help="Lower temperature in Kelvin",
    )
    parser.add_argument(
        "--high-temp",
        metavar="T",
        default=298.15,
        type=float,
        help="Higher temperature in Kelvin",
    )
    parser.add_argument(
        "--boltzmann",
        "-k",
        metavar="K",
        default=constants.BOLTZMANN_K,
        type=float,
        help="Value of the Boltzmann constant to use.",
    )
    parser.add_argument(
        "--points",
        "-n",
        metavar="N",
        default=100,
        type=int,
        help="Number of points to use in each graph.",
    )
    parser.add_argument(
        "--depth",
        metavar="N",
        default=10,
        type=int,
        help="The depth of the Metropolis algorithm, if chosen.",
    )
    parser.add_argument(
        "--mc-points",
        metavar="N",
        default=1000,
        type=int,
        help="Points to check the Metropolis algorithm at.",
    )
    parser.add_argument(
        "--backend",
        choices=["monte-carlo", "c", "python"],
        default="c",
        help="Select which backend to use.",
    )
    parser.add_argument(
        "--threads",
        metavar="N",
        default=max(32, 4 + os.cpu_count()),
        type=int,
        help="Number of threads to use.",
    )
    if pass_args is None:
        args = vars(parser.parse_args())
    else:
        args = vars(parser.parse_args(pass_args))

    thermo.PlotValsMethod.getsingleton().setstrat(
        thermo.ThreadedStrategy.getsingleton()
    )
    if args["backend"] == "monte-carlo":
        thermo.ThermoMethod.getsingleton().setstrat(
            montecarlo.MetropolisStrategy.getsingleton()
        )
        montecarlo.MetropolisStrategy.getsingleton().setpoints(args["mc_points"])
        montecarlo.MetropolisStrategy.getsingleton().setdepth(args["depth"])
    elif args["backend"] == "c":
        thermo.PlotValsMethod.getsingleton().setstrat(
            fastcwrapper.CPlotStrategy.getsingleton()
        )
    elif args["backend"] == "python":
        pass

    try:
        thermo.PlotValsMethod.getsingleton().getstrat().setthreads(args["threads"])
    except AttributeError:
        pass

    temps = np.linspace(args["low_temp"], args["high_temp"], args["points"])
    ens, endev, magdev = thermo.PlotValsMethod.getsingleton().calc_plot_vals(
        hamiltonian.PeriodicHamiltonian(args["coupling"], args["magnet"]),
        args["length"],
        temps,
    )
    plot.figure()
    plot.plot(temps, ens, label="Energy")
    plot.xlabel("Temperature")
    plot.ylabel("Energy")
    plot.legend()
    plot.figure()
    plot.plot(temps, endev, label="Heat Capacity")
    plot.xlabel("Temperature")
    plot.ylabel("Energy per Temperature")
    plot.legend()
    plot.figure()
    plot.plot(temps, magdev, label="Magnetic Susceptibility")
    plot.xlabel("Temperature")
    plot.ylabel("Energy per Temperature")
    plot.legend()
    if not test:
        plot.show()
        sys.exit()
    return ens, endev, magdev


if __name__ == "__main__":
    main()
