#!/bin/bash
#SBATCH -J SineWall
#SBATCH -t 05:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH -o SW-%j

DATADIR=/home/ms2674/SineWall-m-002-la20/

SCRATCH=/scratch/ms2674/SineWall-m-002-la20/

# Set the openfoam environment variables
source /usr/local/OpenFOAM/OpenFOAM-8/etc/bashrc

rm -rf $SCRATCH
# make scratch space for yourself and specific to this run
mkdir -p $SCRATCH
chmod -R 700 $SCRATCH
echo "directory made and permisions are set!"

# report back to yourself the name of the node the calculation is 
# running and the time it starts

/usr/bin/hostname > /home/ms2674/SineWall-m-002-la20/nodeinfo.log
/usr/bin/date >> /home/ms2674/SineWall-m-002-la20/nodeinfo.log

# copy the case files to the node
cp -rf $DATADIR $SCRATCH/..
cd $SCRATCH


echo "START mesh generation ....."
echo "-----> Create background mesh with blockMesh"
blockMesh > $DATADIR/log.blockMesh

echo "------> scale down to micron size"
transformPoints -scale "(0.001 0.001 0.001)" > $DATADIR/log.transformPoints
echo "-----> Prepare case for automatic mesh refinement"
rm -rf 0 const*/polyMesh/refine*

echo "END mesh generation ....."

echo "START Processing ....."
echo "-----> Copy 0.orig directory to new 0 directory" 
rm -rf 0
cp -R 0.orig 0
echo "-----> set the intial water level"
setFields > $DATADIR/log.setFields
echo "-----> Decompose case on 4 cores"
decomposePar -force > $DATADIR/log.decomposePar
(echo "-----> Run de solver interFoam on 4 cores on :" && date)
mpirun -np 24 interFoam -parallel > $DATADIR/log.interFoam 2>&1
(echo "-----> End of solver calculation on :" && date)

echo "END Processing ....."
reconstructParMesh > $DATADIR/log.MeshReconstruct
reconstructPar > $DATADIR/log.Reconstruct

##### REPORT BACK, COPY THE RESULTS and CLEAN UP

echo "Job Done" >> $DATADIR/nodeinfo.log
/bin/date >> $DATADIR/nodeinfo.log

cp -r $SCRATCH $DATADIR

rm -rf $SCRATCH
