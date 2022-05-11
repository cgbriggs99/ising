/*
 *  fastcmodule.c
 *  Author: Connor Briggs (cgbriggs@vt.edu)
 *  
 *  C backend for the Ising problem. It should be super fast.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "ising.h"
#include <stdio.h>
#include <errno.h>

PyObject *fastc_energy(PyObject *self, PyObject *args) {
  int sp, pos;
  double coupling, magnet, result;

  int ret = PyArg_ParseTuple(args, "iidd", &sp, &pos, &coupling, &magnet);

  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_energy!");
    return (NULL);
  }
  result = energy((uint32_t) sp, pos, coupling, magnet);
  return (PyFloat_FromDouble(result));
}

PyObject *fastc_magnet(PyObject *self, PyObject *args) {
  int sp, pos, result;

  int ret = PyArg_ParseTuple(args, "ii", &sp, &pos);

  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_magnet!");
    return (NULL);
  }
  result = magnet((uint32_t) sp, pos);
  return (PyLong_FromLong(result));
}

PyObject *fastc_p_partition(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;
  PyErr_Clear();

  int ret = PyArg_ParseTuple(args, "iddddi", &length, &coupling, &magnet,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_p_partition!");
    return (NULL);
  }
  double ret2 = p_partition(length, coupling, magnet,
			    temp, boltzmann, threads);
  printf("partition: %f\n", ret2);
  fflush(stdout);
  return (PyFloat_FromDouble(ret2));
}

PyObject *fastc_p_average(PyObject *self, PyObject *args) {
  int length;
  double temp, boltzmann, coupling, magnet;
  PyObject *func, *exc, *out;
  PyErr_Clear();
  errno = 0;

  int ret = PyArg_ParseTuple(args, "Oidddd", &func, &length, &coupling, &magnet,
			     &temp, &boltzmann);
  exc = PyErr_Occurred();
  if(!ret || exc != NULL || errno != 0) {
    PyErr_Print();
    perror("PyArg_ParseTuple did not return 0 in fastc_p_average!");
    return (NULL);
  }
  double ret2 = p_average(func, length, coupling, magnet, temp, boltzmann);
  if(isnan(ret2)) {
    PyErr_Print();
    perror("Result was NaN!");
    return (NULL);
  }
  out = PyFloat_FromDouble(ret2);
  exc = PyErr_Occurred();
  if(out == NULL || exc != NULL) {
    PyErr_Print();
    perror("Could not create float object!");
    return (NULL);
  }
  return (out);
}

PyObject *fastc_p_variance(PyObject *self, PyObject *args) {
  int length;
  double temp, boltzmann, coupling, magnet;
  PyObject *func, *out, *exc;

  PyErr_Clear();
  int ret = PyArg_ParseTuple(args, "Oidddd", &func, &length, &coupling, &magnet,
			     &temp, &boltzmann);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_p_variance!");
    return (NULL);
  }

  double ret2 = p_variance(func, length, coupling, magnet, temp, boltzmann);
  if(isnan(ret2)) {
    PyErr_Print();
    perror("Result was NaN!");
    return (NULL);
  }
  out = PyFloat_FromDouble(ret2);
  exc = PyErr_Occurred();
  if(out == NULL || exc != NULL) {
    PyErr_Print();
    perror("Could not create float object!");
    return (NULL);
  }
  return (out);
}

// Docstring in FastcMethods
PyObject *fastc_p_plots(PyObject *self, PyObject *args) {
  int positions, len, i, threads;
  double coupling, magnet, boltzmann;
  double *temps, *energies, *heats, *magsus;
  PyObject *temps_obj, *hold, *ens_list,
    *heats_list, *magsus_list;

  PyErr_Clear();
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
  ret = p_plots(positions, coupling, magnet, boltzmann,
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
  // If any are not able to be allocated, die.
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
    fprintf(stderr, "%d items\n", len);
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
  // Free up resources. I hope there are no leaks.
  free(energies);
  free(heats);
  free(magsus);
  free(temps);
  
  return (PyTuple_Pack(3, ens_list, heats_list, magsus_list));
}

// Makes things work.
static PyMethodDef FastcMethods[] = {
  {"p_plots", fastc_p_plots, METH_VARARGS, "Pass the Ising plotting function"
   " to C.\n"
   ":param int positions: The number of spin positions.\n"
   ":param float coupling: Spin coupling constant.\n"
   ":param float magnet: Spin magnetization constant.\n"
   ":param temps: Temperatures to use.\n"
   ":type temps: list(float)\n"
   ":param float boltzmann: The Boltzmann constant.\n"
   ":param int threads: Number of threads to use.\n"
   ":return: Three lists of energies, heats, and magnetic susceptibilities.\n"},
  {"p_partition", fastc_p_partition, METH_VARARGS, ""},
  {"p_average", fastc_p_average, METH_VARARGS, ""},
  {"p_variance", fastc_p_variance, METH_VARARGS, ""},
  {"energy", fastc_energy, METH_VARARGS, "Find the energy of a configuration "
   "as C would find it.\n"
   ":param int sp: The spin configuration.\n"
   ":param int pos: The number of positions.\n"
   ":param double coupling: The spin coupling constant.\n"
   ":param double magnet: The magnetization constant.\n"},
  {"magnet", fastc_magnet, METH_VARARGS, "Find the magnetization of a configuration.\n"
   ":param int sp: The spin configuration.\n"
   ":param int length: The number of positions.\n"},
  {NULL, NULL, 0, NULL}
};

// Makes things work.
static struct PyModuleDef fastcmodule = {
  PyModuleDef_HEAD_INIT,
  "fastc",
  "Contains C bindings for ising functions.",
  -1,
  FastcMethods
};

// Makes things work.
PyMODINIT_FUNC PyInit_fastc(void) {
  return PyModule_Create(&fastcmodule);
}
