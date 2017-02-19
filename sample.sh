#!/usr/bin/bash
cuda=$1
if [ "$cuda"x = ""x ];
then
cuda=7.5
fi
export LD_LIBRARY_PATH=/usr/local/cuda-$cuda/lib64
cp -r /usr/src/gie_samples ./
cd gie_samples/samples
make
cd bin
echo "Running giexec"
./giexec --model=../data/samples/googlenet/googlenet.caffemodel  --deploy=../data/samples/googlenet/googlenet.prototxt --output=prob
echo "Running giexec_debug"
./giexec_debug --model=../data/samples/googlenet/googlenet.caffemodel  --deploy=../data/samples/googlenet/googlenet.prototxt --output=prob

samples="sample_char_rnn sample_char_rnn_debug sample_googlenet sample_googlenet_debug sample_mnist sample_mnist_debug sample_mnist_api sample_mnist_api_debug sample_plugin sample_plugin_debug"
for sample in $samples
do
	echo "&&&&RUNNING ************************ $sample *************************"
	./$sample
done
