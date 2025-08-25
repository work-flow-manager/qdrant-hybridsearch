 Iniciando com CUDA 11.8 (compatível com Easypanel)
===========================================
📊 Verificando GPU...
PyTorch: 2.1.0+cu118
CUDA compilado: 11.8
CUDA disponível: False
⚠️ GPU não disponível - usando CPU
⚠️ nvidia-ml-py: GPU não acessível

📦 Carregando modelos...
/usr/local/lib/python3.11/dist-packages/transformers/utils/hub.py:123: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
  warnings.warn(
Carregando modelo denso...
.gitattributes: 1.63kB [00:00, 15.1MB/s]
config.json: 100%|██████████| 201/201 [00:00<00:00, 2.56MB/s]
README.md: 160kB [00:00, 326MB/s]
config.json: 100%|██████████| 690/690 [00:00<00:00, 7.48MB/s]
INFO:     127.0.0.1:53648 - "GET /health HTTP/1.1" 200 OK
model.safetensors: 100%|██████████| 2.24G/2.24G [00:19<00:00, 116MB/s] 
config.json: 100%|██████████| 688/688 [00:00<00:00, 9.88MB/s]
model.onnx: 100%|██████████| 546k/546k [00:00<00:00, 107MB/s]
model.onnx_data: 100%|██████████| 2.24G/2.24G [00:19<00:00, 115MB/s] 
model_O4.onnx: 100%|██████████| 80.6k/80.6k [00:00<00:00, 94.6MB/s]
INFO:     127.0.0.1:43196 - "GET /health HTTP/1.1" 200 OK
model_qint8_avx512_vnni.onnx: 100%|██████████| 562M/562M [00:04<00:00, 113MB/s] 
sentencepiece.bpe.model: 100%|██████████| 5.07M/5.07M [00:00<00:00, 108MB/s]
special_tokens_map.json: 100%|██████████| 280/280 [00:00<00:00, 2.55MB/s]
tokenizer.json: 100%|██████████| 17.1M/17.1M [00:00<00:00, 117MB/s]
tokenizer_config.json: 100%|██████████| 418/418 [00:00<00:00, 6.28MB/s]
openvino_model.bin: 100%|██████████| 2.24G/2.24G [00:19<00:00, 115MB/s] 
openvino_model.xml: 713kB [00:00, 546MB/s]
INFO:     127.0.0.1:46630 - "GET /health HTTP/1.1" 200 OK
pytorch_model.bin: 100%|██████████| 2.24G/2.24G [00:19<00:00, 115MB/s] 
sentence_bert_config.json: 100%|██████████| 57.0/57.0 [00:00<00:00, 395kB/s]
sentencepiece.bpe.model: 100%|██████████| 5.07M/5.07M [00:00<00:00, 118MB/s]
special_tokens_map.json: 100%|██████████| 280/280 [00:00<00:00, 2.97MB/s]
tokenizer.json: 100%|██████████| 17.1M/17.1M [00:00<00:00, 117MB/s]
tokenizer_config.json: 100%|██████████| 418/418 [00:00<00:00, 5.57MB/s]
modules.json: 100%|██████████| 387/387 [00:00<00:00, 5.09MB/s]
✅ Modelo denso carregado
Carregando modelo esparso...
tokenizer_config.json: 100%|██████████| 348/348 [00:00<00:00, 3.42MB/s]
vocab.txt: 232kB [00:00, 120MB/s]
tokenizer.json: 712kB [00:00, 243MB/s]
special_tokens_map.json: 100%|██████████| 125/125 [00:00<00:00, 1.75MB/s]
config.json: 100%|██████████| 774/774 [00:00<00:00, 12.4MB/s]
pytorch_model.bin: 100%|██████████| 438M/438M [00:04<00:00, 99.1MB/s] 
generation_config.json: 100%|██████████| 90.0/90.0 [00:00<00:00, 1.17MB/s]
✅ Modelo esparso carregado

✅ Iniciando API...
===========================================
/usr/local/lib/python3.11/dist-packages/transformers/utils/hub.py:123: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
  warnings.warn(
INFO:     Started server process [1]
INFO:     Waiting for application startup.
GPU not available, using CPU
Error creating collection: [Errno 111] Connection refused
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:47116 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:47128 - "GET /health HTTP/1.1" 200 OK
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [1]
INFO:     127.0.0.1:35722 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40466 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:56162 - "GET /health HTTP/1.1" 200 OK
