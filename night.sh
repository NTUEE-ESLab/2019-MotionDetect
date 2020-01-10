export NO_CUDA=1
export NO_DISTRIBUTED=1
git clone --recursive https://github.com/pytorch/pytorch
cd pytorch
git submodule update --remote third_party/protobuf
python3 setup.py build
echo raspberry | sudo -E python3 setup.py install

