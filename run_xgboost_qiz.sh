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

a=0
b=1
c=2

# level 1
$BIN xgboost.conf num_round=150 data=$CAT_TRAIN$a eval[test]=$CAT_TRAIN$a
$BIN xgboost.conf task=pred model_in=0150.model test:data=$CAT_TEST
cp pred.txt pred_cat_level1.txt0
$BIN xgboost.conf num_round=150 data=$CAT_TRAIN$b eval[test]=$CAT_TRAIN$b
$BIN xgboost.conf task=pred model_in=0150.model test:data=$CAT_TEST
cp pred.txt pred_cat_level1.txt1
$BIN xgboost.conf num_round=150 data=$CAT_TRAIN$c eval[test]=$CAT_TRAIN$c
$BIN xgboost.conf task=pred model_in=0150.model test:data=$CAT_TEST
cp pred.txt pred_cat_level1.txt2
python generate_pred_ratio_train.py pred_cat_level1.txt $CAT_LABEL ../raw_data/projects.csv $CAT_QIZ


$BIN xgboost.conf num_round=150 data=$DOG_TRAIN$a eval[test]=$DOG_TRAIN$a
$BIN xgboost.conf task=pred model_in=0150.model test:data=$DOG_TEST
cp pred.txt pred_dog_level1.txt0
$BIN xgboost.conf num_round=150 data=$DOG_TRAIN$b eval[test]=$DOG_TRAIN$b
$BIN xgboost.conf task=pred model_in=0150.model test:data=$DOG_TEST
cp pred.txt pred_dog_level1.txt1
$BIN xgboost.conf num_round=150 data=$DOG_TRAIN$c eval[test]=$DOG_TRAIN$c
$BIN xgboost.conf task=pred model_in=0150.model test:data=$DOG_TEST
cp pred.txt pred_dog_level1.txt2
python generate_pred_ratio_train.py pred_dog_level1.txt $DOG_LABEL ../raw_data/projects.csv $DOG_QIZ

echo "dog result1:"
python ../evaluate/construct.py pred_dog_level1.txt0 $DOG_LABEL $RESULT
python ../evaluate/metric_AUC.py $DOG_LABEL $RESULT
python ../evaluate/construct.py pred_dog_level1.txt1 $DOG_LABEL $RESULT
python ../evaluate/metric_AUC.py $DOG_LABEL $RESULT
python ../evaluate/construct.py pred_dog_level1.txt2 $DOG_LABEL $RESULT
python ../evaluate/metric_AUC.py $DOG_LABEL $RESULT

echo "pig level1:"
$BIN xgboost.conf num_round=150 data=$PIG_TRAIN$a eval[test]=$PIG_TRAIN$a
$BIN xgboost.conf task=pred model_in=0150.model test:data=$PIG_TEST
cp pred.txt pred_pig_level1.txt0
$BIN xgboost.conf num_round=150 data=$PIG_TRAIN$b eval[test]=$PIG_TRAIN$b
$BIN xgboost.conf task=pred model_in=0150.model test:data=$PIG_TEST
cp pred.txt pred_pig_level1.txt1
$BIN xgboost.conf num_round=150 data=$PIG_TRAIN$c eval[test]=$PIG_TRAIN$c
$BIN xgboost.conf task=pred model_in=0150.model test:data=$PIG_TEST
cp pred.txt pred_pig_level1.txt2
python generate_pred_ratio_train.py pred_pig_level1.txt $PIG_LABEL ../raw_data/projects.csv $PIG_QIZ

# level 2
$BIN xgboost.conf num_round=150 data=$CAT_QIZ eval[test]=$CAT_QIZ
mv 0150.model level2.model

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
