#/usr/bin/env bash -e

config="./config.ini"
config_default="./config.ini.default"
if [ ! -f "$config" ]
then
    cp $config_default $config
fi

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python2`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    virtualenv -p $PYTHON $VENV

fi

. $VENV/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade hermes-python
