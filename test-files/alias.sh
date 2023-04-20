VERBOSE=5
# TERSE=--terse-print-dir
# unset TERSE

if [[ "${VIRTUAL_ENV}" != */grammar-tool-* ]] ; then
    poetry shell
    # NOTE: spawns a new shell, source again to get aliases
fi

GT_PYTHON=python3

if [ -e this.pegen -o -e start.pegen ] ; then
    export GT_STYLE=pegen
elif [ -e this.gram -o -e start.gram ] ; then
    export GT_STYLE=pegen
elif [ -e this.peg -o -e start.peg ] ; then
    export GT_STYLE=peg
elif [ -e this.lark -o -e start.lark ] ; then
    export GT_STYLE=lark
elif [ -e this.g4 -o -e start.g4 ] ; then
    export GT_STYLE=antlr4
else
    unset GT_STYLE
fi

export GT_OPT="--verbose ${VERBOSE} ${TERSE} "

export GT_STYLE_OPT="--style ${GT_STYLE}"

alias rc='      . tool/test-files/alias.sh'

export PYPATH_TOOL=' export PYTHONPATH=.:tool:../tool '

#alias gt='      ${PYPATH_TOOL} && tool/s/scripts/grammar-tool.sh '
alias gt='      ${PYPATH_TOOL} && time ${GT_PYTHON} -m grammar_tool '
alias pyt='     ${PYPATH_TOOL} && time python3 -m grammar_tool '
alias cpt='     ${PYPATH_TOOL} && time pypy3 -m grammar_tool '

alias use-pypy='export GT_PYTHON=pypy3 '
alias use-cpy=' export GT_PYTHON=python3 '
alias use-numba=' export GT_PYTHON=numba '

alias gbld='    gt --all ${GT_OPT} ${GT_STYLE_OPT} build              2>&1 '
alias gtst='    gt --all ${GT_OPT} ${GT_STYLE_OPT} test               2>&1 '

alias all='     export GT_ALL=--all '
alias xall='    unset GT_ALL '

all

alias gxc='     gt ${GT_ALL} ${GT_OPT} ${GT_STYLE_OPT} clean          2>&1 '
alias gxi='     gt ${GT_ALL} ${GT_OPT} ${GT_STYLE_OPT} --clean init   2>&1 '
alias gxm='     gt ${GT_ALL} ${GT_OPT} ${GT_STYLE_OPT} compose        2>&1 '
alias gxb='     gt ${GT_ALL} ${GT_OPT} ${GT_STYLE_OPT} build          2>&1 '
alias gmk='     ( cd work ; make 2>&1 )'
alias gxt='     gt ${GT_ALL} ${GT_OPT} ${GT_STYLE_OPT} test           2>&1 '

alias tst_prep_0='( cp tool/s/generator/${GT_STYLE}/model/tests/astpatch.py test_this.py work/tests/. )'
alias tst_prep_1='( cp tool/s/generator/${GT_STYLE}/model/tests/parser.py test_this.py work/tests/. )'
alias tst_prep_2=" cd work && ${PYPATH_TOOL} "
alias tst_prep=" tst_prep_1 && tst_prep_2 "
alias tst='(    tst_prep && pytest -vvv      2>&1 )'
alias cov='(    tst_prep && pytest --cov-report term-missing --cov 2>&1 )'
alias cxm='(    tst_prep && coverage run --cov-report term-missing tests/test_this.py 2>&1 )'
alias cxh='(    tst_prep && coverage html --cov-report term-missing tests/test_this.py 2>&1 )'
alias cxr='(    tst_prep && coverage report  -m tests/test_this.py 2>&1 )'
alias lnt='(    tst_prep && pylint tests/test_this.py 2>&1 )'

alias atst='(   clear && out=raw.ansi && ( tst_prep && script -c "pytest -v" ../${out} ) ; strip-cr ${out} ; emacs ${out} )'

# alias tox_g1='( copy -r grammar/grammar work/. )'
# alias tox_g2='( copy -r grammar/grammar work/tests/. )'
alias tox_g1='( mkdir -p work/grammar && cp work/grammar{,/__init__}.py )'
alias tox_prep='( gxb && clear && copy -r setup.* tox.ini work/. && tox_g1 )'
alias rtxt='(   raw-to-text < raw.dat > err.txt )'
alias txo='(    tox_prep && cd work && script -c "${PYPATH_TOOL} && tox" | tee raw.dat 2>&1 ; rtxt )'
alias tx0='(    tox_prep && cd work && script -c "${PYPATH_TOOL} && tox -rvve py310" | tee raw.dat 2>&1 ; rtxt )'

alias fme='(    clear && script -c "${PYPATH_TOOL} && python3 -m coverage run match-examples.py" ; rtxt )'

