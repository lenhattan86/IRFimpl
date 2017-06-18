# configure
./config
# CPU
#bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package
# GPU
bazel build --config=opt --config=cuda //tensorflow/tools/pip_package:build_pip_package --cxxopt="-D_GLIBCXX_USE_CXX11_ABI=0"
