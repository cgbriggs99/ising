 
#include <stdio.h>
#include <stdlib.h>
#include "ising.h"
#include <Python.h>
#include <stdint.h>

int main(void) {
  double *ens = calloc(10, sizeof(double)),
    *heat = calloc(10, sizeof(double)),
    *mag = calloc(10, sizeof(double)),
    *temps = calloc(10, sizeof(double));

  for(int i = 0; i < 10; i++) {
    temps[i] = 0.1 + 20 * i;
  }
  
  int ret0 = p_plots(4, -2, 1.1, 1, temps, 10, ens, heat, mag, 4);
  free(ens);
  free(heat);
  free(mag);
  free(temps);
  printf("ens: [ ");
  for(int i = 0; i < 10; i++) {
    printf("%f", ens[i]);
    if(i != 9) {
      printf(", ");
    }
  }
  printf(" ]\nheat: [");
  for(int i = 0; i < 10; i++) {
    printf("%f", heat[i]);
    if(i != 9) {
      printf(", ");
    }
  }
  printf(" ]\nmag: [");
  for(int i = 0; i < 10; i++) {
    printf("%f", mag[i]);
    if(i != 9) {
      printf(", ");
    }
  }
  printf(" ]\n");
  double ret1 = p_partition(4, -2, 1.1, 298.15, 1, 4);
  printf("%f\n", ret1);
  fflush(stdout);
  return (ret0);
}
