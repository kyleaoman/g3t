
function db_1e5(){
    export DB=/tmp/ciao_1e4_23_06_2018.sql
    export LIM=1e4
}

function Box0mr_bao(){
    export INTRO="module load python/3.5_anaconda_nompi"
    export NAME=/HydroSims/Magneticum/Box0/mr_bao/
    export SSH_HOST='di29bop2@c2paplogin.lrz.de'
    export INTRO="module load python/3.5_anaconda_nompi"
    export SCRATCH=/gpfs/work/pr86re/di29bop2
    export BASE=/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_bao
    export TOSQL=tmp/magneticum.sql
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
