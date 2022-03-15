/*
 *  fafbmodule.c
 *  Author: Connor Briggs (cgbriggs@vt.edu)
 *  
 *  C backend for the Ising problem. It should be fast as f*** boiiiii.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "ising.h"
#include <stdio.h>

PyObject *fafb_pass_to_c(PyObject *self, PyObject *args) {
  int positions, len, i, threads;
  double coupling, magnet, boltzmann;
  double *temps, *energies, *heats, *magsus;
  PyObject *temps_obj, *hold, *out_tuple, *ens_list,
    *heats_list, *magsus_list;

  // Parse the arguments.
  int ret = PyArg_ParseTuple(args, "iddOdi", &positions,
		       &coupling, &magnet, &temps_obj, &boltzmann,
			     &threads);
  if(!ret) {
    perror("Did not return 0.");
    return (NULL);
  }
  // Load the temperatures into a C array.
  temps = calloc(PyList_Size(temps_obj), sizeof(double));
  len = PyList_Size(temps_obj);
  for(i = 0; i < len; i++) {
    hold = PyList_GetItem(temps_obj, i);
    temps[i] = PyFloat_AsDouble(hold);
  }

  // Prep the output arrays.
  energies = calloc(len, sizeof(double));
  heats = calloc(len, sizeof(double));
  magsus = calloc(len, sizeof(double));

  // Calculate the values.
  ret = threaded_ising(positions, coupling, magnet, boltzmann,
		       temps, len, energies, heats, magsus, threads);
  if(ret) {
    free(energies);
    free(heats);
    free(magsus);
    free(temps);
    perror("Thread did not return 0.");
    return (NULL);
  }

  ens_list = PyList_New(len);
  heats_list = PyList_New(len);
  magsus_list = PyList_New(len);
  if(ens_list == NULL) {
    perror("Could not allocate first list.");
  }
  if(heats_list == NULL) {
    perror("Could not allocate second list.");
  }
  if(magsus_list == NULL) {
    perror("Could not allocate third list.");
  }
  if(ens_list == NULL || heats_list == NULL || magsus_list == NULL) {
    free(energies);
    free(heats);
    free(magsus);
    free(temps);
    return (NULL);
  }

  char buff[1025] = {0};
  // Put the data from the C arrays into Python arrays.
  for(i = 0; i < len; i++) {
    int ret1 = PyList_SetItem(ens_list, i, PyFloat_FromDouble(energies[i])),
      ret2 = PyList_SetItem(heats_list, i, PyFloat_FromDouble(heats[i])),
      ret3 = PyList_SetItem(magsus_list, i, PyFloat_FromDouble(magsus[i]));
    if(ret1 || ret2 || ret3) {
      free(energies);
      free(heats);
      free(magsus);
      sprintf(buff, "%d %d %d\nCould not set item %d.", ret1, ret2, ret3, i);
      perror(buff);
      return (NULL);
    }
  }
  free(energies);
  free(heats);
  free(magsus);
  free(temps);
  
  return (PyTuple_Pack(3, ens_list, heats_list, magsus_list));
}

static PyMethodDef FafbMethods[] = {
  {"plot_vals", fafb_pass_to_c, METH_VARARGS, "Pass the Ising plotting function"
   " to C.\n"
   ":param int positions: The number of spin positions.\n"
   ":param float coupling: Spin coupling constant.\n"
   ":param float magnet: Spin magnetization constant.\n"
   ":param temps: Temperatures to use.\n"
   ":type temps: list(float)\n"
   ":param float boltzmann: The Boltzmann constant.\n"
   ":param int threads: Number of threads to use.\n"
   ":return: Three lists of energies, heats, and magnetic susceptibilities.\n"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fafbmodule = {
  PyModuleDef_HEAD_INIT,
  "fafb",
  "Contains C bindings for ising functions.",
  -1,
  FafbMethods
};

PyMODINIT_FUNC PyInit_fafb(void) {
  return PyModule_Create(&fafbmodule);
}
