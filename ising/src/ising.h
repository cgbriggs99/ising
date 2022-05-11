/*
 *  ising.h
 *  Author: Connor Briggs (cgbriggs@vt.edu)
 *  
 *  Contains prototypes for Ising code.
 */

#ifndef __ISING_H__
#define __ISING_H__

#include <Python.h>

typedef struct {
  double *taylor_matrix;
  int len;
  int dim;
} graph_ham_t;

/*
 * Compute values for energy, heat capacity, and magnetic susceptibility at
 * the given grid points and with the given coupling constants.
 */
extern int np_plots(int positions, double coupling, double magnet,
		      double boltzmann, double const *temps, int len_temps,
			  double *out_ens, double *out_heat, double *mag_sus,
			  int threads);

extern int p_plots(int positions, double coupling, double magnet,
		      double boltzmann, double const *temps, int len_temps,
			  double *out_ens, double *out_heat, double *mag_sus,
			  int threads);

extern int graph_plots(int positions, graph_ham_t *ham,
		      double boltzmann, double const *temps, int len_temps,
			  double *out_ens, double *out_heat, double *mag_sus,
			  int threads);

extern int gen_plots(int positions, PyObject *ham,
		      double boltzmann, double const *temps, int len_temps,
			  double *out_ens, double *out_heat, double *mag_sus,
			  int threads);

extern double np_partition(int positions, double coupling,
				    double magnet, double temp,
				 double boltzmann);

extern double np_average(PyObject *func,
			       int positions,
			       double coupling, double magnet,
				  double temp, double boltzmann);

extern double np_variance(PyObject *func,
				int positions,
				double coupling, double magnet,
				   double temp, double boltzmann);

extern double p_partition(int positions, double coupling,
				   double magnet, double temp,
				 double boltzmann);

extern double p_average(PyObject *func,
			       int positions,
			       double coupling, double magnet,
				 double temp, double boltzmann);

extern double p_variance(PyObject *func,
				int positions,
				double coupling, double magnet,
				  double temp, double boltzmann);

extern int make_graph_ham(PyObject *const ham, graph_ham_t *out);

extern int delete_graph_ham(graph_ham_t *__restrict__ in);

extern double graph_partition(graph_ham_t *const ham, int positions,
				       double temp, double boltzmann);

extern double graph_average(PyObject *func,
				     graph_ham_t *const ham, int positions,
				       double temp, double boltzmann);

extern double graph_variance(PyObject *func,
				     graph_ham_t *const ham, int positions,
				       double temp, double boltzmann);

extern double gen_partition(PyObject *ham, int positions,
				     double temp, double boltzmann);

extern double gen_average(PyObject *func,
			    PyObject *ham, int positions,
				     double temp, double boltzmann);

extern double gen_variance(PyObject *func,
			    PyObject *ham, int positions,
				     double temp, double boltzmann);
#endif
