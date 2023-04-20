alias rc='. tool/test-files/section/alias.sh'

alias gt=' b=./tool && PYTHONPATH=${b} ${b}/scripts/grammar-tool '

alias c=' gt clean '
alias ini=' gt --clean init '
alias comp=' gt compose '
alias b=' gt build '

alias tst='( cd work ; pytest )'
