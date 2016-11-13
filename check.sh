#!/bin/bash
DIR=/home/yiwen/stockStrategies
cd ${DIR}
echo $(date +'%Y-%m-%d') >> job.res
echo 'LongHu' >> job.res
echo '===============================' >>job.res
cat longhu/job.log|grep Records >> job.res
echo '' >>job.res
echo 'DaZong' >> job.res
echo '===============================' >>job.res
cat dazong/job.log|grep Records >> job.res
echo '' >>job.res
echo 'JuPai' >> job.res
echo '===============================' >>job.res
cat jupai/job.log|grep Records >> job.res
echo '' >>job.res
echo 'ZengChi' >> job.res
echo '===============================' >>job.res
cat zengchi/job.log|grep Records >> job.res
echo '' >>job.res
echo 'PuoFa' >> job.res
echo '===============================' >>job.res
cat puofa/job.log|grep Records >> job.res
echo '' >>job.res
echo 'GuDong' >> job.res
echo '===============================' >>job.res
cat gudong/job.log|grep Records >> job.res
echo '' >>job.res

sh dazong/output.sh >> job.res
sh longhu/output.sh >> job.res
sh zengchi/output.sh >> job.res
sh jupai/output.sh >> job.res
sh addition/output.sh >> job.res
sh puofa/output.sh >> job.res
sh gudong/output.sh >> job.res
java -cp javamail-attachment-1.0-SNAPSHOT-jar-with-dependencies.jar JavaMailWithAttachment $(date +'%Y-%m-%d') $(date +'%Y-%m-%d') dazong/dazong.csv longhu/longhu.csv zengchi/zengchi.csv jupai/jupai.csv addition/zengfa.csv puofa/puofa.csv gudong/gudong.csv false >> job.res
