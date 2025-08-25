Ação
Commit: Fix: Identificado problema real - Driver 575.64 suporta CUDA 12.9!

DESCOBERTA IMPORTANTE:
- Driver NVIDIA: 575.64.03 (NÃO é 11.8!)
- CUDA suportado: 12.9
- GPU detectada: Quadro RTX 4000
- Docker vê GPU perfeitamente com --gpus all

Problema real: Easypanel não está passando GPU para container
- Precisa configurar runtime nvidia
- Ou mapear devices /dev/nvidia*
- Ou usar privileged: true

Solução:
- Use Dockerfile.cuda12 (CUDA 12.1 compatível)
- Configure GPU no Easypanel ou rode fora dele

GPU está funcionando perfeitamente no sistema! 
##########################################
### Download Github Archive Started...
### Mon, 25 Aug 2025 21:00:45 GMT
##########################################

#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile.cuda12
#1 DONE 0.0s

#1 [internal] load build definition from Dockerfile.cuda12
#1 transferring dockerfile: 5.38kB done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04
#2 DONE 0.6s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [ 1/11] FROM docker.io/nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04@sha256:f3a7fb39fa3ffbe54da713dd2e93063885e5be2f4586a705c39031b8284d379a
#4 CACHED

#5 [internal] load build context
#5 transferring context: 31.48kB done
#5 DONE 0.0s

#6 [ 2/11] RUN apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     python3.11-distutils     git     curl     gcc     g++     cuda-toolkit-12-1     && rm -rf /var/lib/apt/lists/*     && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1     && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
#6 0.074 Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1581 B]
#6 0.101 Get:2 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [1940 kB]
#6 0.315 Get:3 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
#6 0.318 Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
#6 0.910 Get:5 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [3253 kB]
#6 1.025 Get:6 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
#6 1.197 Get:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
#6 1.369 Get:8 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
#6 1.666 Get:9 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [5235 kB]
#6 1.843 Get:10 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1271 kB]
#6 1.876 Get:11 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [48.5 kB]
#6 2.351 Get:12 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
#6 2.351 Get:13 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
#6 2.352 Get:14 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
#6 2.488 Get:15 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1575 kB]
#6 2.504 Get:16 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [3569 kB]
#6 2.684 Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [5430 kB]
#6 2.851 Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [75.9 kB]
#6 2.854 Get:19 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [83.2 kB]
#6 2.855 Get:20 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.2 kB]
#6 2.963 Fetched 42.9 MB in 3s (14.8 MB/s)
#6 2.963 Reading package lists...
#6 3.399 Reading package lists...
#6 3.816 Building dependency tree...
#6 3.919 Reading state information...
#6 3.966 Some packages could not be installed. This may mean that you have
#6 3.966 requested an impossible situation or if you are using the unstable
#6 3.966 distribution that some required packages have not yet been created
#6 3.966 or been moved out of Incoming.
#6 3.966 The following information may help to resolve the situation:
#6 3.966 
#6 3.966 The following packages have unmet dependencies:
#6 4.009  cuda-libraries-12-1 : Depends: libcublas-12-1 (>= 12.1.3.1) but 12.1.0.26-1 is to be installed
#6 4.009  libcublas-dev-12-1 : Depends: libcublas-12-1 (>= 12.1.3.1) but 12.1.0.26-1 is to be installed
#6 4.012 E: Unable to correct problems, you have held broken packages.
#6 ERROR: process "/bin/sh -c apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     python3.11-distutils     git     curl     gcc     g++     cuda-toolkit-12-1     && rm -rf /var/lib/apt/lists/*     && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1     && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1" did not complete successfully: exit code: 100
------
 > [ 2/11] RUN apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     python3.11-distutils     git     curl     gcc     g++     cuda-toolkit-12-1     && rm -rf /var/lib/apt/lists/*     && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1     && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1:
3.966 Some packages could not be installed. This may mean that you have
3.966 requested an impossible situation or if you are using the unstable
3.966 distribution that some required packages have not yet been created
3.966 or been moved out of Incoming.
3.966 The following information may help to resolve the situation:
3.966 
3.966 The following packages have unmet dependencies:
4.009  cuda-libraries-12-1 : Depends: libcublas-12-1 (>= 12.1.3.1) but 12.1.0.26-1 is to be installed
4.009  libcublas-dev-12-1 : Depends: libcublas-12-1 (>= 12.1.3.1) but 12.1.0.26-1 is to be installed
4.012 E: Unable to correct problems, you have held broken packages.
------
Dockerfile.cuda12:18
--------------------
  17 |     # Instalar Python 3.11 e CUDA toolkit
  18 | >>> RUN apt-get update && apt-get install -y \
  19 | >>>     python3.11 \
  20 | >>>     python3.11-dev \
  21 | >>>     python3-pip \
  22 | >>>     python3.11-distutils \
  23 | >>>     git \
  24 | >>>     curl \
  25 | >>>     gcc \
  26 | >>>     g++ \
  27 | >>>     # Adicionar ferramentas CUDA
  28 | >>>     cuda-toolkit-12-1 \
  29 | >>>     && rm -rf /var/lib/apt/lists/* \
  30 | >>>     && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
  31 | >>>     && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
  32 |     
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     python3.11-distutils     git     curl     gcc     g++     cuda-toolkit-12-1     && rm -rf /var/lib/apt/lists/*     && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1     && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1" did not complete successfully: exit code: 100
##########################################
### Error
### Mon, 25 Aug 2025 21:00:50 GMT
##########################################

Command failed with exit code 1: docker buildx build --network host -f /etc/easypanel/projects/app/qdrant-gpu/code/Dockerfile.cuda12 -t easypanel/app/qdrant-gpu --label 'keep=true' --build-arg 'GIT_SHA=8db742e0c818523bd670fcabb91cf727458649da' /etc/easypanel/projects/app/qdrant-gpu/code/