#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <omp.h>
#include <vector>
#include "likwid-stuff.h"

const char* dgemm_desc = "Blocked dgemm, OpenMP-enabled";


/* This routine performs a dgemm operation
 *  C := C + A * B
 * where A, B, and C are n-by-n matrices stored in row-major format.
 * On exit, A and B maintain their input values. */
void square_dgemm_blocked(int n, int block_size, double* A, double* B, double* C) 
{
   // insert your code here: implementation of blocked matrix multiply with copy optimization and OpenMP parallelism enabled

   // be sure to include LIKWID_MARKER_START(MY_MARKER_REGION_NAME) inside the block of parallel code,
   // but before your matrix multiply code, and then include LIKWID_MARKER_STOP(MY_MARKER_REGION_NAME)
   // after the matrix multiply code but before the end of the parallel code block.
 int num_blocks = n / block_size;

    LIKWID_MARKER_INIT;

    #pragma omp parallel
    {
        // Each thread gets its own copy buffers
        std::vector<double> A_cache(block_size * block_size);
        std::vector<double> B_cache(block_size * block_size);
        std::vector<double> C_cache(block_size * block_size);

        LIKWID_MARKER_THREADINIT;
        LIKWID_MARKER_START(MY_MARKER_REGION_NAME);

        #pragma omp for
        for (int i = 0; i < num_blocks; i++) {
            for (int j = 0; j < num_blocks; j++) {

                // Load C block into cache
                for (int block_i = 0; block_i < block_size; block_i++) {
                    for (int block_j = 0; block_j < block_size; block_j++) {
                        C_cache[block_i * block_size + block_j] =
                            C[(i * block_size + block_i) * n + (j * block_size + block_j)];
                    }
                }

                for (int k = 0; k < num_blocks; k++) {

                    // Load A into cache
                    for (int block_i = 0; block_i < block_size; block_i++) {
                        for (int block_k = 0; block_k < block_size; block_k++) {
                            A_cache[block_i * block_size + block_k] =
                                A[(i * block_size + block_i) * n + (k * block_size + block_k)];
                        }
                    }

                    // Load B into cache
                    for (int block_k = 0; block_k < block_size; block_k++) {
                        for (int block_j = 0; block_j < block_size; block_j++) {
                            B_cache[block_k * block_size + block_j] =
                                B[(k * block_size + block_k) * n + (j * block_size + block_j)];
                        }
                    }

                    // Perform the multiplication of the blocks
                    for (int block_i = 0; block_i < block_size; block_i++) {
                        for (int block_j = 0; block_j < block_size; block_j++) {
                            for (int block_k = 0; block_k < block_size; block_k++) {
                                C_cache[block_i * block_size + block_j] +=
                                    A_cache[block_i * block_size + block_k] *
                                    B_cache[block_k * block_size + block_j];
                            }
                        }
                    }
                }

                // Store updated C block
                for (int block_i = 0; block_i < block_size; block_i++) {
                    for (int block_j = 0; block_j < block_size; block_j++) {
                        C[(i * block_size + block_i) * n + (j * block_size + block_j)] =
                            C_cache[block_i * block_size + block_j];
                    }
                }
            }
        }

        LIKWID_MARKER_STOP(MY_MARKER_REGION_NAME);
    }

   std::cout << "Insert your blocked matrix multiply with copy optimization, openmp-parallel edition here " << std::endl;
}
