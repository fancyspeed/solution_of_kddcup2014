BIN=../../tools/libfm/bin/libFM

TRAIN=qiz_cat.svm
VALID=$TRAIN
TEST=qiz_dog.svm
LABEL=test_dog.label
PRED=pred.txt
RESULT=../result/libfm.csv

# MCMC
$BIN -task r -train $TRAIN -validation $VALID -test $TEST -out $PRED -dim '1,1,4' -method mcmc -iter 100 -init_stdev 0 -verbosity 1

python ../evaluate/construct.py $PRED $LABEL $RESULT
python ../evaluate/metric_AUC.py $LABEL $RESULT

TRAIN=qiz_dog.svm
VALID=$TRAIN
TEST=qiz_pig.svm
LABEL=test_pig.label
PRED=pred.txt
RESULT=../result/libfm.csv

# MCMC
$BIN -task r -train $TRAIN -validation $VALID -test $TEST -out $PRED -dim '1,1,4' -method mcmc -iter 100 -init_stdev 0 -verbosity 1

python ../evaluate/construct.py $PRED $LABEL $RESULT
cd ../result/
rm ./kdd_fm.zip
zip kdd_fm.zip libfm.csv
