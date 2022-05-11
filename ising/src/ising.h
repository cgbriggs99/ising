/*
 *  ising.h
 *  Author: Connor Briggs (cgbriggs@vt.edu)
 *  
 *  Contains prototypes for Ising code.
 */

#ifndef __ISING_H__
#define __ISING_H__

#ifndef NO_PYTHON
#include <Python.h>
#endif

typedef struct {
  double *taylor_matrix;
  int len;
} graph_ham_t;

/*
 * Compute values for energy, heat capacity, and magnetic susceptibility at
 * the given grid points and with the given coupling constants.
 */

extern double energy(uint32_t spinconf, int positions, double coupling, double magnet);

extern int magnet(uint32_t sp, int pos);

extern int p_plots(int positions, double coupling, double magnet,
		      double boltzmann, double const *temps, int len_temps,
			  double *out_ens, double *out_heat, double *mag_sus,
			  int threads);

extern double p_partition(int positions, double coupling,
				   double magnet, double temp,
			  double boltzmann, int threads);

#ifndef NO_PYTHON
extern double p_average(PyObject *func,
			       int positions,
			       double coupling, double magnet,
			double temp, double boltzmann);

extern double p_variance(PyObject *func,
				int positions,
				double coupling, double magnet,
			 double temp, double boltzmann);
#endif
#endif
