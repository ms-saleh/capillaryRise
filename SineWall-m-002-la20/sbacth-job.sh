#!/bin/bash

# make scratch space for yourself an specific to this run
mkdir /scratch/ms2674/SineWall-m-002-la20/

# report back to yourself the name of the node the calculation is 
# running and the time it starts

/usr/bin/hostname > /home/ms2674/SineWall-m-002-la20/nodeinfo.log
/usr/bin/date >> /home/ms2674/SineWall-m-002-la20/nodeinfo.log

# copy the case files to the node
cp -r /home/ms2674/SineWall-m-002-la20/ /scratch/ms2674/SineWall-m-002-la20/
cd /scratch/ms2674/SineWall-m-002-la20/

###   ***SET SBATCH PARAMETERS****

#SBATCH -J sbatch-job
#SBATCH -t 00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
NCORES=16
# Set the openfoam environment variables
source /usr/local/OpenFOAM/OpenFOAM-8/etc/bashrc


cd ${0%/*} || exit 1                        # Run from this directory
. $WM_PROJECT_DIR/bin/tools/RunFunctions    # Tutorial run functions


echo "START mesh generation ....."
echo "-----> Create .foam file for post-processing"
touch tuto.foam

echo "-----> Create background mesh with blockMesh"
blockMesh > log.blockMesh

echo "------> scale down to micron size"
transformPoints -scale "(0.001 0.001 0.001)" >
echo "-----> scaled gemotery by 0.001 "
echo "-----> Prepare case for automatic mesh refinement"
rm -rf 0 const*/polyMesh/refine*

echo "END mesh generation ....."

echo "START Processing ....."
echo "-----> Copy 0.orig directory to new 0 directory" 
rm -rf 0
cp -R 0.orig 0
echo "-----> set the intial water level"
setFields > log.setFields
echo "-----> Decompose case on 4 cores"
decomposePar -force > log.decomposePar
(echo "-----> Run de solver interFoam on 4 cores on :" && date)
srun -n $NCORES -N 1 interFoam -parallel > log.interFoam_file 2>&1
(echo "-----> End of solver calculation on :" && date)

echo "END Processing ....."
reconstructParMesh > log.MeshReconstruct
reconstructPar > log.Reconstruct





##### REPORT BACK, COPY THE RESULTS and CLEAN UP

echo "Job Done" >> /home/ms2674/SineWall-m-002-la20/nodeinfo.log
/bin/date >> /home/ms2674/SineWall-m-002-la20/nodeinfo.log

cp -r /scratch/ms2674/SineWall-m-002-la20/ /home/ms2674/SineWall-m-002-la20/

cp -rf /scratch/ms2674/SineWall-m-002-la20/
