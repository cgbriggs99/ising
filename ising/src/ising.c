/*
 *  ising.c
 *  Author: Connor Briggs (cgbriggs@vt.edu)
 *  
 *  Contains definitions for Ising code.
 */

#include <stdlib.h>
#include <math.h>
#ifdef _WIN32
#  include <windows.h>
#else
#  include <pthread.h>
#endif
#include "ising.h"
#include <stdio.h>
#include <stdint.h>
#ifndef NO_PYTHON
#  include <Python.h>
#endif

// Structures the data to pass to each thread.
typedef struct {
  int index, threads;
  int positions, len;
  double coupling, magnet, boltzmann;
  double const *temps;
  double *out_ens, *out_heat, *out_magsus;
} pass_args_t;

typedef struct {
  int index, threads;
  int positions, len;
  double coupling, magnet, boltzmann, temp;
  double *sum;
} pass_args_small_t;

#ifndef NO_PYTHON
typedef struct {
  int index, threads, positions, len;
  double coupling, magnet, boltzmann, temp;
  double *sum, *partition;
  PyObject *func;
} pass_args_avg_t;

typedef struct {
  int index, threads, positions, len;
  double coupling, magnet, boltzmann, temp;
  double *sum1, *sum2, *partition;
  PyObject *func;
} pass_args_var_t;
#endif

// Precomputed bit counts.
static char bit_counts[] = { 0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4,
			    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
			    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
			    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
			    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
			    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
			    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
			    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
			    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
			    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
			    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
			    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
			    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
			    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
			    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
			    4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8 };

// Splits a 32 bit value into 8 bit chunks.
typedef struct {
  uint8_t a: 8, b:8, c:8, d:8;
} bitvec_32_t;

// Convert between the two.
typedef union {
  uint32_t in;
  bitvec_32_t vec;
} conv_t;

// Count the number of active bits.
static inline int bitcount(uint32_t in) {
  conv_t conv;
  conv.in = in;
  bitvec_32_t vec = conv.vec;
  return (bit_counts[vec.a] + bit_counts[vec.b] + bit_counts[vec.c] +
	  bit_counts[vec.d]);
}

// Do this operation quickly. See ising.spins.SpinConfig.magnetization for source
#define MAGNETIZATION(I, L) ((bitcount((uint32_t) I) * 2) - L)

// Do this in bit operations instead of multiplications.
#define P_SPINCOUPLE(I, L) ((bitcount((uint32_t) (((I << (L - 1)) | I >> 1) ^ ~I) & ~((0xffffffff) << L)) * 2) - L)

double energy(uint32_t sp, int pos, double coupling, double magnet) {
  double mag = MAGNETIZATION(sp, pos);
  double coup = P_SPINCOUPLE(sp, pos);
  return (-coupling * coup + magnet * mag);
}

int magnet(uint32_t sp, int pos) {
  int on = bitcount(sp & (0xffffffff >> (32 - pos))),
    off = bitcount(~sp & (0xffffffff >> (32 - pos)));
  return (on - off);
}

static inline int jcouple(uint32_t sp, int pos) {
  uint32_t mask = sp << (pos - 1) | sp >> 1;
  mask ^= sp;
  mask &= ~(0xffffffff << pos);
  return (bitcount(mask) * 2 - pos);
}


// Compute the energies, heat capacities, and magnetic susceptibilities.
#ifdef _WIN32
static DWORD p_compute_vals(void *arg) {
#else
static void *p_compute_vals(void *arg) {
#endif
  pass_args_t *pass = (pass_args_t *) arg;

  for(int i = pass->index; i < pass->len; i += pass->threads) {
    double part = 0, energy = 0, heat = 0, magsus = 0, magav = 0,
      expo = 0, en = 0, mag = 0;
    for(int j = 0; j < (1 << pass->positions); j++) {
      mag = MAGNETIZATION(j, pass->positions);
      en = -pass->coupling * P_SPINCOUPLE(j, pass->positions) +
	pass->magnet * mag;
      expo = exp(-en / (pass->temps[i] * pass->boltzmann));
      part += expo;
      energy += expo * en;
      heat += en * en * expo;
      magsus += mag * mag * expo;
      magav += mag * expo;
    }
    pass->out_ens[i] = energy / part;
    pass->out_heat[i] = (heat / part - (energy / part) * (energy / part)) /
      (pass->temps[i] * pass->temps[i] *  pass->boltzmann);
    pass->out_magsus[i] = (magsus / part - magav * magav / (part * part)) /
      (pass->temps[i] * pass->boltzmann);
  }
  return (0);
}

// Documentation in ising.h
int p_plots(int positions, double coupling, double magnet,
		      double boltzmann, double const *temps, int len_temps,
		   double *out_ens, double *out_heat, double *mag_sus,
		   int threads) {

  // This thread is also going to be used, which is why it's threads - 1.
#ifdef _WIN32
  HANDLE *thread = calloc(threads - 1, sizeof(HANDLE));
  DWORD *ids = calloc(threads - 1, sizeof(DWORD));
#else
  pthread_t *thread = calloc(threads - 1, sizeof(pthread_t));
  pthread_attr_t *attr = calloc(threads - 1, sizeof(pthread_attr_t));
#endif
  
  pass_args_t *pass_args = calloc(threads, sizeof(pass_args_t));
  void *rets;

  // Set up and run the threads.
  for(int i = 0; i < threads; i++) {
    pass_args[i].index = i;
    pass_args[i].threads = threads;
    pass_args[i].positions = positions;
    pass_args[i].len = len_temps;
    pass_args[i].coupling = coupling;
    pass_args[i].magnet = magnet;
    pass_args[i].boltzmann = boltzmann;
    pass_args[i].temps = temps;
    pass_args[i].out_ens = out_ens;
    pass_args[i].out_heat = out_heat;
    pass_args[i].out_magsus = mag_sus;
    if(i != threads - 1) {
#ifdef _WIN32
      thread[i] = CreateThread(NULL, 0, p_compute_vals, &(pass_args[i]), 0,
			    &(ids[i]));
#else
      pthread_attr_init(&(attr[i]));
      pthread_create(&(thread[i]), &(attr[i]), p_compute_vals, &(pass_args[i]));
#endif
    }
  }

  // Don't leave this thread all alone. It needs work too.
  p_compute_vals(&(pass_args[threads - 1]));

#ifdef _WIN32
  WaitForMultipleObjects(threads - 1, thread, TRUE, INFINITE);
#else
  for(int i = 0; i < threads - 1; i++) {
    pthread_join(thread[i], &rets);
  }
#endif
    
  // I hope there are no leaks.
#ifdef _WIN32
  free(thread);
  free(pass_args);
  free(ids);
#else
  free(pass_args);
  free(thread);
  free(attr);
#endif

  return (0);
}

#ifdef _WIN32
static DWORD p_compute_partition(void *arg) {
#else
static void *p_compute_partition(void *arg) {
#endif

  pass_args_small_t *pass = (pass_args_small_t *) arg;

  for(int i = pass->index; i < pass->len; i += pass->threads) {
    double mag = MAGNETIZATION(i, pass->positions);
    double energy = -pass->coupling * P_SPINCOUPLE(i, pass->positions) +
      pass->magnet * mag;
    *(pass->sum) += exp(-energy / (pass->boltzmann * pass->temp));
  }
  return (0);
}
 
double p_partition(int positions, double coupling, double magnet, double temp,
		   double boltzmann, int threads) {
#ifdef _WIN32
  HANDLE *thread = calloc(threads - 1, sizeof(HANDLE));
  DWORD *ids = calloc(threads - 1, sizeof(DWORD));
#else
  pthread_t *thread = calloc(threads - 1, sizeof(pthread_t));
  pthread_attr_t *attr = calloc(threads - 1, sizeof(pthread_attr_t));
#endif
  double *sum = calloc(threads, sizeof(double));
  double out;
  pass_args_small_t *pass_args = calloc(threads, sizeof(pass_args_small_t));
  void *rets;

  // Set up and run the threads.
  for(int i = 0; i < threads; i++) {
    pass_args[i].index = i;
    pass_args[i].threads = threads;
    pass_args[i].positions = positions;
    pass_args[i].len = 1 << positions;
    pass_args[i].coupling = coupling;
    pass_args[i].magnet = magnet;
    pass_args[i].boltzmann = boltzmann;
    pass_args[i].temp = temp;
    pass_args[i].sum = &sum[i];
    if(i != threads - 1) {
#ifdef _WIN32
      thread[i] = CreateThread(NULL, 0, p_compute_partition, &(pass_args[i]), 0,
			    &(ids[i]));
#else
      pthread_attr_init(&(attr[i]));
      pthread_create(&(thread[i]), &(attr[i]), p_compute_partition, &(pass_args[i]));
#endif
    }
  }

  // Don't leave this thread all alone. It needs work too.
  p_compute_partition(&(pass_args[threads - 1]));

#ifdef _WIN32
  WaitForMultipleObjects(threads - 1, thread, TRUE, INFINITE);
#else
  for(int i = 0; i < threads - 1; i++) {
    pthread_join(thread[i], &rets);
  }
#endif
    
  // I hope there are no leaks.
#ifdef _WIN32
  free(thread);
  free(pass_args);
  free(ids);
#else
  free(pass_args);
  free(thread);
  free(attr);
#endif
  out = 0;
  for(int i = 0; i < threads; i++) {
    out += sum[i];
  }
  free(sum);

  return (out);
}

#ifndef NO_PYTHON

double p_average(PyObject *func, int positions, double coupling, double magnet,
		 double temp, double boltzmann) {
  double num = 0, den = 0;
  PyObject *exc, *obj;
  PyErr_Clear();
  for(int i = 0; i < 1 << positions; i++) {
    double mag = MAGNETIZATION(i, positions);
    double energy = -coupling * P_SPINCOUPLE(i, positions) + magnet * mag;
    double expo = exp(-energy / (temp * boltzmann));
    obj = PyObject_CallFunction(func, "i", i);
    if(obj == NULL) {
      perror("Error when calling function!");
      return (NAN);
    }
    num += PyFloat_AsDouble(obj) * expo;
    exc = PyErr_Occurred();
    if(exc != NULL) {
      perror("Error with creation of float!");
      return (NAN);
    }
    den += expo;
  }
  return (num / den);
}

double p_variance(PyObject *func, int positions, double coupling, double magnet,
		  double temp, double boltzmann) {
  double num1 = 0, num2 = 0, den = 0;
  for(int i = 0; i < 1 << positions; i++) {
    double mag = MAGNETIZATION(i, positions);
    double energy = -coupling * P_SPINCOUPLE(i, positions) + magnet * mag;
    double expo = exp(-energy / (temp * boltzmann));
    double f = PyFloat_AsDouble(PyObject_CallFunction(func, "i", i));

    num1 += f * expo;
    num2 += f * f * expo;
    den += expo;
  }
  return (num2 / den - num1 * num1 / den / den);
}

#endif
