#set -v
F=$SCRATCH/$TARGET
mkdir -p output
rsync -arv --exclude=__pycache__ --cvs-exclude  --exclude=tmp $SSH_HOST:$F/output/ output





