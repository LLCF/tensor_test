#!/usr/bin/bash
cuda=$1
export LD_LIBRARY_PATH=/usr/local/cuda-$cuda/lib64
cd cuda/_tests/gie_tests/
mkdir -p  build-cuda-$cuda/x86_64
cp  infer_caffe infer_caffe_static build-cuda-$cuda/x86_64/
sudo mount -t cifs -o username=kevin,password=kevin,noperm //10.19.193.205/manual /mnt/
ln -s /mnt/gie_data data
echo "************************ infer_test ******************************"
./infer_test 2>&1 | tee infer_test.log
echo "***************************giexec** ******************************"
./giexec --model=data/samples/googlenet/googlenet.caffemodel --deploy=data/samples/googlenet/googlenet.prototxt  --output=prob 2>&1 | tee giexec.log
echo "*********************FP16 FP32 static desktop**************************"
python scripts/testAllNetworks.py x86_64 cuda-$cuda FP16 static desktop 2>&1 | tee FP16_static.log
python scripts/testAllNetworks.py x86_64 cuda-$cuda FP32 static desktop 2>&1 | tee FP32_static.log
python scripts/testAllNetworks.py x86_64 cuda-$cuda FP32 dynamic desktop 2>&1 | tee FP32_dynamic.log
python scripts/testAllNetworks.py x86_64 cuda-$cuda FP16 dynamic desktop  2>&1 | tee FP16_dynamic.log

echo "************************ infer_layer ******************************"
gie_install_path=/usr/include/x86_64-linux-gnu/
python scripts/batch_tester.py -d $gie_install_path/NvInfer.h -e ./infer_layer -o failure_report_layer.log --verbose


mkdir result
cp *.log *.txt result/
cp *.log *.txt ../../../
