BIN=../../tools/xgboost/xgboost

CAT_TRAIN=train_cat.svm
CAT_TEST=test_cat.svm
CAT_QIZ=qiz_cat.svm
CAT_LABEL=test_cat.label

DOG_TRAIN=train_dog.svm
DOG_TEST=test_dog.svm
DOG_LABEL=test_dog.label
DOG_QIZ=qiz_dog.svm

PIG_TRAIN=train_pig.svm
PIG_TEST=test_pig.svm
PIG_LABEL=test_pig.label
PIG_QIZ=qiz_pig.svm

PRED=pred.txt
RESULT=../result/xgboost.csv

$BIN xgboost.conf num_round=50 data=$CAT_QIZ eval[test]=$CAT_QIZ
mv 0050.model level2.model

$BIN xgboost.conf task=pred model_in=level2.model test:data=$DOG_QIZ
cp pred.txt pred_dog_level2.txt

echo "dog result2:"
python ../evaluate/construct.py $PRED $DOG_LABEL $RESULT
python ../evaluate/metric_AUC.py $DOG_LABEL $RESULT

echo "pig level2:"
$BIN xgboost.conf task=pred model_in=level2.model test:data=$PIG_QIZ
cp pred.txt pred_pig_level2.txt

python ../evaluate/construct.py $PRED $PIG_LABEL $RESULT
cd ../result/
rm ./kdd_xgboost.zip
zip kdd_xgboost.zip xgboost.csv
