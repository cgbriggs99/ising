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

PyObject *fastc_np_plots(PyObject *self, PyObject *args) {
  int num_temps, length, threads, i;
  double *temps, coupling, magnet, boltzmann;
  double *out_ens, *out_heats, *out_mags;
  PyObject *in_temps, *energies, *magsuses, *heatcaps, *out,
    *curr, *iter;

  int ret = PyArg_ParseTuple(args, "iddOdi", &length, &coupling,
			     &magnet, &in_temps, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_plots!");
    return (NULL);
  }
  
  num_temps = PyObject_Length(in_temps);
  iter = PyObject_GetIter(in_temps);
  if(iter == NULL) {
    perror("Could not get the iterator in fastc_np_plots!");
    return (NULL);
  }

  // No length.
  if(num_temps == -1) {
    temps = malloc(0);
    num_temps = 0;
    PyErr_Clear();
    curr = PyIter_Next(iter);
    while(curr != NULL) {
      temps = realloc(temps, (num_temps + 1) * sizeof(double));
      temps[num_temps] = PyFloat_AsDouble(curr);
      num_temps++;
      curr = PyIter_Next(iter);
    }
  } else { // Has length.
    temps = malloc(num_temps * sizeof(double));
    i = 0;
    curr = PyIter_Next(iter);
    while(i < num_temps && curr != NULL) {
      temps[i] = PyFloat_AsDouble(curr);
      i++;
      curr = PyIter_Next(iter);
    }
    if(i != num_temps - 1) {
      free(temps);
      return (NULL);
    }
  }
  out_ens = malloc(num_temps * sizeof(double));
  out_heats = malloc(num_temps * sizeof(double));
  out_mags = malloc(num_temps * sizeof(double));

  ret = np_plots(length, coupling, magnet, boltzmann, temps, len_temps,
		 out_ens, out_heats, out_mags, threads);
  if(ret != 0) {
    perror("Failed to compute plots!");
    free(out_ens);
    free(out_heats);
    free(out_mags);
    free(temps);
    return (NULL);
  }

  energies = PyList_New(len_temps);
  heatcaps = PyList_New(len_temps);
  magsuses = PyList_New(len_temps);

  if(energies == NULL || heatcaps == NULL || magsuses == NULL) {
    perror("Could not allocate output arrays!");
    free(out_ens);
    free(out_heats);
    free(out_mags);
    free(temps);
    return (NULL);
  }

  for(i = 0; i < len_temps; i++) {
    PyList_SetItem(energies, i, PyFloat_FromDouble(out_ens[i]));
    PyList_SetItem(heatcaps, i, PyFloat_FromDouble(out_heats[i]));
    PyList_SetItem(magsuses, i, PyFloat_FromDouble(out_mags[i]));
  }

  free(temps);
  free(out_heats);
  free(out_mags);
  free(out_ens);

  return (PyTuple_Pack(3, energies, heatcaps, magsuses));
}
    
PyObject *fastc_p_plots(PyObject *self, PyObject *args) {
  int num_temps, length, threads, i;
  double *temps, coupling, magnet, boltzmann;
  double *out_ens, *out_heats, *out_mags;
  PyObject *in_temps, *energies, *magsuses, *heatcaps, *out,
    *curr, *iter;

  int ret = PyArg_ParseTuple(args, "iddOdi", &length, &coupling,
			     &magnet, &in_temps, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_plots!");
    return (NULL);
  }
  
  num_temps = PyObject_Length(in_temps);
  iter = PyObject_GetIter(in_temps);
  if(iter == NULL) {
    perror("Could not get the iterator in fastc_np_plots!");
    return (NULL);
  }

  // No length.
  if(num_temps == -1) {
    temps = malloc(0);
    num_temps = 0;
    PyErr_Clear();
    curr = PyIter_Next(iter);
    while(curr != NULL) {
      temps = realloc(temps, (num_temps + 1) * sizeof(double));
      temps[num_temps] = PyFloat_AsDouble(curr);
      num_temps++;
      curr = PyIter_Next(iter);
    }
  } else { // Has length.
    temps = malloc(num_temps * sizeof(double));
    i = 0;
    curr = PyIter_Next(iter);
    while(i < num_temps && curr != NULL) {
      temps[i] = PyFloat_AsDouble(curr);
      i++;
      curr = PyIter_Next(iter);
    }
    if(i != num_temps - 1) {
      free(temps);
      return (NULL);
    }
  }
  out_ens = malloc(num_temps * sizeof(double));
  out_heats = malloc(num_temps * sizeof(double));
  out_mags = malloc(num_temps * sizeof(double));

  ret = p_plots(length, coupling, magnet, boltzmann, temps, len_temps,
		 out_ens, out_heats, out_mags, threads);
  if(ret != 0) {
    perror("Failed to compute plots!");
    free(out_ens);
    free(out_heats);
    free(out_mags);
    free(temps);
    return (NULL);
  }

  energies = PyList_New(len_temps);
  heatcaps = PyList_New(len_temps);
  magsuses = PyList_New(len_temps);

  if(energies == NULL || heatcaps == NULL || magsuses == NULL) {
    perror("Could not allocate output arrays!");
    free(out_ens);
    free(out_heats);
    free(out_mags);
    free(temps);
    return (NULL);
  }

  for(i = 0; i < len_temps; i++) {
    PyList_SetItem(energies, i, PyFloat_FromDouble(out_ens[i]));
    PyList_SetItem(heatcaps, i, PyFloat_FromDouble(out_heats[i]));
    PyList_SetItem(magsuses, i, PyFloat_FromDouble(out_mags[i]));
  }

  free(temps);
  free(out_heats);
  free(out_mags);
  free(out_ens);

  return (PyTuple_Pack(3, energies, heatcaps, magsuses));
}    

PyObject *fastc_np_partition(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;

  int ret = PyArg_ParseTuple(args, "iddddi", &length, &coupling, &magnet,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(np_partition(length, coupling, magnet,
					  temp, boltzmann, threads)));
}

PyObject *fastc_np_average(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;
  PyObject *func;

  int ret = PyArg_ParseTuple(args, "Oiddddi", &func, &length, &coupling, &magnet,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(np_average(func, length, coupling, magnet,
					temp, boltzmann, threads)));
}

PyObject *fastc_np_variance(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;
  PyObject *func;

  int ret = PyArg_ParseTuple(args, "Oiddddi", &func, &length, &coupling, &magnet,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(np_variance(func, length, coupling, magnet,
					 temp, boltzmann, threads)));
}

PyObject *fastc_p_partition(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;

  int ret = PyArg_ParseTuple(args, "iddddi", &length, &coupling, &magnet,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(p_partition(length, coupling, magnet,
					 temp, boltzmann, threads)));
}

PyObject *fastc_p_average(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;
  PyObject *func;

  int ret = PyArg_ParseTuple(args, "Oiddddi", &func, &length, &coupling, &magnet,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(p_average(func, length, coupling, magnet,
				       temp, boltzmann, threads)));
}

PyObject *fastc_p_variance(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;
  PyObject *func;

  int ret = PyArg_ParseTuple(args, "Oiddddi", &func, &length, &coupling, &magnet,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(p_variance(func, length, coupling, magnet,
					temp, boltzmann, threads)));
}

PyObject *fastc_graph_partition(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;
  PyObject *ham;
  graph_ham_t *hamilt = malloc(sizeof(graph_ham_t));
  make_graph_ham(ham, hamilt); 

  int ret = PyArg_ParseTuple(args, "iOddi", &length, &ham,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  PyObject *out = PyFloat_FromDouble(graph_partition(length, hamilt,
						     temp, boltzmann, threads));
  delete_graph_ham(hamilt);
  free(hamilt);
  return (out);
}

PyObject *fastc_graph_average(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;
  PyObject *ham, *func;
  graph_ham_t *hamilt = malloc(sizeof(graph_ham_t));
  make_graph_ham(ham, hamilt); 

  int ret = PyArg_ParseTuple(args, "OiOddi", &func, &length, &ham,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  PyObject *out = PyFloat_FromDouble(graph_average(func, length, hamilt,
						   temp, boltzmann, threads));
  delete_graph_ham(hamilt);
  free(hamilt);
  return (out);
}

PyObject *fastc_graph_variance(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann, coupling, magnet;
  PyObject *ham, *func;
  graph_ham_t *hamilt = malloc(sizeof(graph_ham_t));
  make_graph_ham(ham, hamilt); 

  int ret = PyArg_ParseTuple(args, "OiOddi", &func, &length, &ham,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  PyObject *out = PyFloat_FromDouble(graph_variance(func, length, hamilt,
						    temp, boltzmann, threads));
  delete_graph_ham(hamilt);
  free(hamilt);
  return (out);
}

PyObject *fastc_gen_partition(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann;
  PyObject *ham;

  int ret = PyArg_ParseTuple(args, "iOddi", &length, &ham,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(gen_partition(length, ham,
					 temp, boltzmann, threads)));
}

PyObject *fastc_gen_average(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann;
  PyObject *ham, *func;

  int ret = PyArg_ParseTuple(args, "oiOddi", &func, &length, &ham,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(gen_average(func, length, ham,
					 temp, boltzmann, threads)));
}

PyObject *fastc_gen_variance(PyObject *self, PyObject *args) {
  int length, threads;
  double temp, boltzmann;
  PyObject *ham, *func;

  int ret = PyArg_ParseTuple(args, "oiOddi", &func, &length, &ham,
			     &temp, &boltzmann, &threads);
  if(!ret) {
    perror("PyArg_ParseTuple did not return 0 in fastc_np_partitions!");
    return (NULL);
  }

  return (PyFloat_FromDouble(gen_variance(func, length, ham,
					 temp, boltzmann, threads)));
}

// Docstring in FastcMethods
PyObject *fastc_pass_to_c(PyObject *self, PyObject *args) {
  int positions, len, i, threads;
  double coupling, magnet, boltzmann;
  double *temps, *energies, *heats, *magsus;
  PyObject *temps_obj, *hold, *ens_list,
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
  {"plot_vals", fastc_pass_to_c, METH_VARARGS, "Pass the Ising plotting function"
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
