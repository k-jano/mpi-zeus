#!/bin/bash -l

frame_per_job=5
frame_per_job_without_one=$(( $frame_per_job - 1))
task_id=$SLURM_ARRAY_TASK_ID
end=$(( $task_id * $frame_per_job))
start=$(( $end - $frame_per_job_without_one))

loadPovray() {
  module add plgrid/apps/povray
}

run() {
  povray Subset_Start_Frame=$start Subset_End_Frame=$end animation_a_.ani
}

loadPovray &&
run