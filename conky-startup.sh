sleep 0s
killall conky

python $HOME/.conky/generate.py
find $HOME/.conky/rc -name \*.rc | xargs -I {} sh -c 'sleep 0.5; conky -c {} & exit'
