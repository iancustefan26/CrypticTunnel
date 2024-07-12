#!/bin/bash

cd src

rsalib="python3 method_convertor.py build_ext --inplace"
aeslib="python3 aes_pybind11_convertor.py build_ext --inplace"

echo "Building C++ Cryptography libraries..."
$rsalib
$aeslib

cd ..

if [ ! -f requirements.txt ]; then
  echo "requirements.txt not found!"
  exit 1
fi

if ! command -v pip &> /dev/null; then
  echo "pip could not be found. Please install pip first."
  exit 1
fi

pip install -r requirements.txt


echo "Finishing...linking command"
cp src/main.py src/cytun
sudo chmod a+rx src/cytun
sudo ln -s src/cytun /usr/local/bin

echo "cytun installed! (CryptoTunnel by Iancu Stefan-Teodor)"

exit 0 
