#!/bin/bash -l

sed -n "${SLURM_ARRAY_TASK_ID}p" < /etc/passwd
