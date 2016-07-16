if [[ $* == *-c* ]]; then
    flags="--with-coverage --cover-html --cover-package=pypriz"
fi

if [[ $1 == "GameEngine" ]]; then
    nosetests test/test_match.py $flags
elif [[ $1 == "flask" ]]; then
    nosetests test/test_flask.py $flags
else
    nosetests test $flags
fi
