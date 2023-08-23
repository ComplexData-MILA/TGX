#!/bin/bash
#SBATCH --partition=main #long
#SBATCH --output=dt%j.txt
#SBATCH --error=dt%jerror.txt 
#SBATCH --cpus-per-task=2                    # Ask for 4 CPUs
#SBATCH --gres=gpu:0                         # Ask for 1 titan xp
#SBATCH --mem=35G                             # Ask for 32 GB of RAM
#SBATCH --time=100:20:00                       # The job will run for 1 day

export HOME="/home/mila/r/razieh.shirzadkhani/tgx"
module load miniconda/3
source $CONDA_ACTIVATE
conda activate /home/mila/r/razieh.shirzadkhani/.conda/envs/tg


pwd
python /home/mila/r/razieh.shirzadkhani/tgx/examples/test.py

