# GPU-Training-Profiling-for-DeepSpeed

This project measures the distributed GPU training time & memory consumption of DeepSpeed's different optimization choices for end-to-end transformer models: 
- stage 0: no optimization, 
- stage 1: optimizer state partitioning, 
- stage 2: gradient partitioning, w/ & w/o offloading, 
- stage 3: parameter partitioning, w/ & w/o offloading. 

By exploring more cofigurations of the training, this project can help building up a cost model of distributed training system.

## Environment Setup
- Install DeepSpeed 
```
pip install deepspeed
``` 
or 
```
pip install transformers[deepspeed]
``` 
- Install Dependencies
```
pip install git+https://github.com/huggingface/transformers
pip install datasets
pip install accelerate
pip install evaluate
pip install sacrebleu
```
- Download Transformers Folder
```
git clone https://github.com/huggingface/transformers.git
```
- References:
  - DeepSeed: https://huggingface.co/docs/transformers/main_classes/deepspeed
  - Transformers: https://huggingface.co/docs/transformers/

## Files
- experiment.sh: The profiling code for different T5 models. It uses nvidia-smi to monitor the memory & power consumption and deepspeed to evaluate the training time of transformer models on NLP tasks.
- extract_latency: Extracting the latency of each configuration. To have more accuracy results, the profiling data of the first 2 iterations of each trainging process is deleted. To have a stable profiling of the training process for large batch_size, the epoch number of large bach size is enlarged.
  - ``` b: batch size ```
  - ``` o: optimization level ```
  - ``` b_new: training epochs ```

- extract_mem: Extracting the memory consumption of each configuration
- de_config_zero0.json: configuration file of DeepSpeed stage 0
- de_config_zero1.json: configuration file of DeepSpeed stage 1
- de_config_zero2.json: configuration file of DeepSpeed stage 2
- de_config_zero3.json: configuration file of DeepSpeed stage 3
- de_config_zero2_offload.json: configuration file of DeepSpeed stage 2 with offloading to CPU
- de_config_zero3_offload.json:configuration file of DeepSpeed stage 3 with offloading to CPU

## Usage
- Profiling: ./experiment.sh. Users need to redefine the ${path_to_transformers_folder}
- Extracting training time: python extract_latency.py, the extracted result will be saved in latency.csv
- Extracting training meme: python extract_mem.py, the extracted result will be saved in mem.csv

The extracted files are as follows: 
```
1, 2, 4, 8, 16, 32, 64, 128: bacth size
```

```
t5-large, t5-3b, t5-11b: different t5 models
```

| optimization_level0 | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 |
|---------------------|---|---|---|---|----|----|----|-----|
| t5-large            |   |   |   |   |    |    |    |     |
| t5-3b               |   |   |   |   |    |    |    |     |
| t5-11b              |   |   |   |   |    |    |    |     |
| optimization_level1 | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 |
| t5-large            |   |   |   |   |    |    |    |     |
| t5-3b               |   |   |   |   |    |    |    |     |
| t5-11b              |   |   |   |   |    |    |    |     |
| optimization_level2 | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 |
| t5-large            |   |   |   |   |    |    |    |     |
| t5-3b               |   |   |   |   |    |    |    |     |
| t5-11b              |   |   |   |   |    |    |    |     |
