/*
 *  ising.h
 *  Author: Connor Briggs (cgbriggs@vt.edu)
 *  
 *  Contains prototypes for Ising code.
 */

#ifndef __ISING_H__
#define __ISING_H__

/*
 * Compute values for energy, heat capacity, and magnetic susceptibility at
 * the given grid points and with the given coupling constants.
 */
extern int threaded_ising(int positions, double coupling, double magnet,
		      double boltzmann, double const *temps, int len_temps,
			  double *out_ens, double *out_heat, double *mag_sus,
			  int threads);

#endif
