model_qint8_avx512_vnni.onnx: 100%|██████████| 562M/562M [00:04<00:00, 117MB/s] 
sentencepiece.bpe.model: 100%|██████████| 5.07M/5.07M [00:00<00:00, 116MB/s]
special_tokens_map.json: 100%|██████████| 280/280 [00:00<00:00, 4.52MB/s]
tokenizer.json: 100%|██████████| 17.1M/17.1M [00:00<00:00, 117MB/s]
tokenizer_config.json: 100%|██████████| 418/418 [00:00<00:00, 3.75MB/s]
openvino_model.bin: 100%|██████████| 2.24G/2.24G [00:19<00:00, 115MB/s] 
openvino_model.xml: 713kB [00:00, 516MB/s]
pytorch_model.bin: 100%|██████████| 2.24G/2.24G [00:19<00:00, 116MB/s] 
sentence_bert_config.json: 100%|██████████| 57.0/57.0 [00:00<00:00, 621kB/s]
sentencepiece.bpe.model: 100%|██████████| 5.07M/5.07M [00:00<00:00, 117MB/s]
special_tokens_map.json: 100%|██████████| 280/280 [00:00<00:00, 5.04MB/s]
tokenizer.json: 100%|██████████| 17.1M/17.1M [00:00<00:00, 117MB/s]
tokenizer_config.json: 100%|██████████| 418/418 [00:00<00:00, 4.70MB/s]
modules.json: 100%|██████████| 387/387 [00:00<00:00, 5.07MB/s]
/usr/local/lib/python3.11/dist-packages/torch/cuda/__init__.py:611: UserWarning: Can't initialize NVML
  warnings.warn("Can't initialize NVML")
/usr/local/lib/python3.11/dist-packages/torch/cuda/__init__.py:740: UserWarning: CUDA initialization: The NVIDIA driver on your system is too old (found version 11080). Please update your GPU driver by downloading and installing a new version from the URL: http://www.nvidia.com/Download/index.aspx Alternatively, go to: https://pytorch.org to install a PyTorch version that has been compiled with your version of the CUDA driver. (Triggered internally at ../c10/cuda/CUDAFunctions.cpp:108.)
  return torch._C._cuda_getDeviceCount() if nvml_count < 0 else nvml_count
✅ Modelo denso carregado
📥 Carregando modelo esparso...
tokenizer_config.json: 100%|██████████| 348/348 [00:00<00:00, 4.62MB/s]
vocab.txt: 232kB [00:00, 142MB/s]
tokenizer.json: 712kB [00:00, 238MB/s]
special_tokens_map.json: 100%|██████████| 125/125 [00:00<00:00, 1.77MB/s]
config.json: 100%|██████████| 774/774 [00:00<00:00, 15.8MB/s]
pytorch_model.bin: 100%|██████████| 438M/438M [00:03<00:00, 117MB/s] 
generation_config.json: 100%|██████████| 90.0/90.0 [00:00<00:00, 1.08MB/s]
✅ Modelo esparso carregado

===========================================
✅ Iniciando API com GPU FORÇADA...
===========================================
/usr/local/lib/python3.11/dist-packages/transformers/utils/hub.py:123: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
  warnings.warn(
INFO:     Started server process [1]
INFO:     Waiting for application startup.
/usr/local/lib/python3.11/dist-packages/torch/cuda/__init__.py:138: UserWarning: CUDA initialization: The NVIDIA driver on your system is too old (found version 11080). Please update your GPU driver by downloading and installing a new version from the URL: http://www.nvidia.com/Download/index.aspx Alternatively, go to: https://pytorch.org to install a PyTorch version that has been compiled with your version of the CUDA driver. (Triggered internally at ../c10/cuda/CUDAFunctions.cpp:108.)
  return torch._C._cuda_getDeviceCount() > 0
GPU not available, using CPU
/usr/local/lib/python3.11/dist-packages/torch/cuda/__init__.py:611: UserWarning: Can't initialize NVML
  warnings.warn("Can't initialize NVML")
Error creating collection: [Errno 111] Connection refused
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:46454 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39068 - "GET /health HTTP/1.1" 200 OK


