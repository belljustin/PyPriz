if [[ $* == *-c* ]]; then
    flags="-v --with-coverage --cover-html --cover-erase --cover-package=pypriz"
fi
if [[ $* == *-l* ]]; then
    flags="$flags --nologcapture" 
fi
if [[ $* == *-p* ]]; then
    flags="$flags --pdb" 
fi

if [[ $1 == "flask" ]]; then
    nosetests test/test_flask.py $flags
else
    nosetests test $flags
fi
