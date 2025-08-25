pytorch_model.bin: 100%|██████████| 2.24G/2.24G [00:19<00:00, 115MB/s] 
sentence_bert_config.json: 100%|██████████| 57.0/57.0 [00:00<00:00, 839kB/s]
sentencepiece.bpe.model: 100%|██████████| 5.07M/5.07M [00:00<00:00, 116MB/s]
special_tokens_map.json: 100%|██████████| 280/280 [00:00<00:00, 4.11MB/s]
tokenizer.json: 100%|██████████| 17.1M/17.1M [00:00<00:00, 116MB/s]
tokenizer_config.json: 100%|██████████| 418/418 [00:00<00:00, 5.33MB/s]
modules.json: 100%|██████████| 387/387 [00:00<00:00, 5.74MB/s]
✓ Dense model carregado
/usr/local/lib/python3.11/dist-packages/transformers/utils/hub.py:123: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
  warnings.warn(
✓ Transformers OK
tokenizer_config.json: 100%|██████████| 348/348 [00:00<00:00, 4.10MB/s]
vocab.txt: 232kB [00:00, 70.4MB/s]
tokenizer.json: 712kB [00:00, 198MB/s]
special_tokens_map.json: 100%|██████████| 125/125 [00:00<00:00, 1.40MB/s]
config.json: 100%|██████████| 774/774 [00:00<00:00, 10.1MB/s]
pytorch_model.bin: 100%|██████████| 438M/438M [00:03<00:00, 116MB/s]  
generation_config.json: 100%|██████████| 90.0/90.0 [00:00<00:00, 1.38MB/s]
✓ Sparse model carregado
✅ Sistema pronto! Iniciando API...
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/usr/local/lib/python3.11/dist-packages/uvicorn/__main__.py", line 4, in <module>
    uvicorn.main()
  File "/usr/local/lib/python3.11/dist-packages/click/core.py", line 1442, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/click/core.py", line 1363, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/click/core.py", line 1226, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/click/core.py", line 794, in invoke
    return callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/uvicorn/main.py", line 416, in main
    run(
  File "/usr/local/lib/python3.11/dist-packages/uvicorn/main.py", line 587, in run
    server.run()
  File "/usr/local/lib/python3.11/dist-packages/uvicorn/server.py", line 61, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/asyncio/runners.py", line 188, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/asyncio/runners.py", line 120, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1517, in uvloop.loop.Loop.run_until_complete
  File "/usr/local/lib/python3.11/dist-packages/uvicorn/server.py", line 68, in serve
    config.load()
  File "/usr/local/lib/python3.11/dist-packages/uvicorn/config.py", line 467, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/uvicorn/importer.py", line 24, in import_from_string
    raise exc from None
  File "/usr/local/lib/python3.11/dist-packages/uvicorn/importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/app/app/main.py", line 14, in <module>
    from app.config import settings
  File "/app/app/config.py", line 5, in <module>
    from pydantic_settings import BaseSettings
ModuleNotFoundError: No module named 'pydantic_settings'

CUDA Version 12.1.0

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.

WARNING: The NVIDIA Driver was not detected.  GPU functionality will not be available.
   Use the NVIDIA Container Toolkit to start this container with GPU support; see
   https://docs.nvidia.com/datacenter/cloud-native/ .

*************************
** DEPRECATION NOTICE! **
*************************
THIS IMAGE IS DEPRECATED and is scheduled for DELETION.
    https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/support-policy.md

🚀 Iniciando com suporte GPU...
📊 Verificando GPU disponível:
CUDA disponível: False
GPU: Não detectada
📦 Verificando modelos...
/usr/local/lib/python3.11/dist-packages/transformers/utils/hub.py:123: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
  warnings.warn(
✓ Sentence Transformers OK
.gitattributes: 1.63kB [00:00, 11.6MB/s]
config.json: 100%|██████████| 201/201 [00:00<00:00, 2.42MB/s]
README.md: 160kB [00:00, 333MB/s]
config.json: 100%|██████████| 690/690 [00:00<00:00, 5.87MB/s]
model.safetensors: 100%|██████████| 2.24G/2.24G [00:19<00:00, 116MB/s] 
config.json: 100%|██████████| 688/688 [00:00<00:00, 7.50MB/s]
model.onnx: 100%|██████████| 546k/546k [00:00<00:00, 125MB/s]