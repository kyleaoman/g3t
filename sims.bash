

function db_1e5_22j(){
    export DB=/tmp/antonio/magneticum.sql.dm
    export LIM=1e4
}

function onc2pap(){
    export PYTHON=python3
    export INTRO="module load python/3.5_intel" #module load python/3.5_anaconda_nompi"
    export SSH_HOST='di29bop2@c2paplogin.lrz.de'
    export SBATCH="llsubmit"
    #export MPIRUN="mpirun -n 1 -ppn 1"
    export MPIRUN=""
    export TEMPLATE="c2papjob.ll"
    export SCRATCH=/gpfs/work/pr86re/di29bop2
    export TOSQL=tmp/magneticum.sql
}


function ondorc1(){
    export PYTHON=python3
    export INTRO="module load python/3.5_intel" #module load python/3.5_intel" #module load python/3.5_anaconda_nompi"
    export SSH_HOST='ragagnin@localhost'
    export SBATCH="bash"
    #export MPIRUN="mpirun -n 1 -ppn 1"
    export MPIRUN=""
    export TEMPLATE="/dev/null"
    export SCRATCH=/tmp/antonio
    export TOSQL=tmp/magneticum.sql
}

function Box0mr_bao(){
    onc2pap
    export LIM=3e4
    export NAME=/HydroSims/Magneticum/Box0/mr_bao/
    export BOXNAME="Box0mr"
    export BASE=/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_bao
}

function Box0mr_bao_z0(){
    Box0mr_bao
    export TAG=z0
    export SNAP=037 
}

function Box0mr_bao_z05(){
    Box0mr_bao
    export TAG=z05
    export SNAP=025 
}


function Box0mr_bao_z1(){
    Box0mr_bao
    export TAG=z1
    export SNAP=014
}

function Box0mr_bao_z15(){
    Box0mr_bao
    export TAG=z15
    export SNAP=012
}

function Box0mr_bao_z2(){
    Box0mr_bao
    export TAG=z2
    export SNAP=010
}




function Box0mr_dm(){
    onc2pap

    export DB=./tmp/magneticum.sql

    export LIM=3e4
    export NAME=/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_dm/
    export BOXNAME="Box0dm"
    export BASE=/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_dm
}

function Box0mr_dm_z0(){
    Box0mr_dm
    export TAG=z0
    export SNAP=037 
}

function Box0mr_dm_z05(){
    Box0mr_dm
    export TAG=z05
    export SNAP=025 
}


function Box0mr_dm_z1(){
    Box0mr_dm
    export TAG=z1
    export SNAP=014
}

function Box0mr_dm_z15(){
    Box0mr_dm
    export TAG=z15
    export SNAP=012
}

function Box0mr_dm_z2(){
    Box0mr_dm
    export TAG=z2
    export SNAP=010
}


function Box2bhr_bao(){
    onc2pap
    export NAME=/HydroSims/Magneticum/Box2b/hr_bao/
    export BOXNAME="Box2bhr"
    export BASE=/smgpfs/work/pr83li/lu78qer5/Magneticum/Box2b/hr_new

}

function Box2bhr_bao_z0(){
    Box2bhr_bao
    export TAG=z0
    export SNAP=031
}

function Box2bhr_bao_z05(){
    Box2bhr_bao
    export TAG=z05
    export SNAP=026
}

function Box2bhr_bao_z1(){
    Box2bhr_bao
    export TAG=z1
    export SNAP=015
}

function Box2bhr_bao_z15(){
    Box2bhr_bao
    export TAG=z15
    export SNAP=012
}
function Box2bhr_bao_z2(){
    Box2bhr_bao
    export TAG=z2
    export SNAP=011
}


function Box4uhr_bao(){
    ondorc1
    export NAME=/HydroSims/Magneticum/Box4/uhr_test/
    export BOXNAME="Box4uhr"
    export BASE=/HydroSims/Magneticum/Box4/uhr_test

}

function Box4uhr_bao_z0(){
    Box4uhr_bao
    export TAG=z0
    export SNAP=136
}

function Box4uhr_bao_z05(){
    Box4uhr_bao
    export TAG=z05
    export SNAP=096
}

function Box4uhr_bao_z1(){
    Box4uhr_bao
    export TAG=z1
    export SNAP=058
}

function Box4uhr_bao_z15(){
    Box4uhr_bao
    export TAG=z15
    export SNAP=044
}

function Box4uhr_bao_z2(){
    Box4uhr_bao
    export TAG=z2
    export SNAP=036
}
