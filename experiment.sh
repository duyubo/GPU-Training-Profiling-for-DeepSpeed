model_array=("t5-large" "t5-3b" "t5-11b")
for b in 1 2 4 8 16 32 64 128
do
	for o in 0 1 2 3
	do
		for model_name in ${model_array[@]}
		do	
			watch -n 0.2 'nvidia-smi | grep "280W" >>  mem_'${b}'_'${o}'_'${model_name}'.log'&
			pid=$!
			echo $pid
			if (( $b > 16 ))
			then
				b_new=$[$b/32]
			else
				b_new=1
			fi
			echo $b_new, "ds_config_zero${o}.json", $model_name
			deepspeed --include="localhost:1" {path_to_transformers_folder}/transformers/examples/pytorch/translation/run_translation.py --deepspeed "ds_config_zero${o}.json"  --model_name_or_path $model_name --per_device_train_batch_size $b --output_dir output_dir --overwrite_output_dir --fp16 --do_train --max_train_samples 500 --num_train_epochs $b_new --dataset_name wmt16 --dataset_config "ro-en" --source_lang en --target_lang ro >> "${b}_${o}_${model_name}.txt"
			sleep 20
			kill -9 $pid
		done
	done
	
done

model_array=("t5-large" "t5-3b" "t5-11b")
for b in 1 2 4 8 16 32 64 128
do
	for o in 2 3
	do
		for model_name in ${model_array[@]}
		do	
			watch -n 0.2 'nvidia-smi | grep "280W" >>  mem_'${b}'_'${o}'_'${model_name}'_offload.log'&
			pid=$!
			echo $pid
			if (( $b > 16))
			then
				b_new=$[$b/32]
			else
				b_new=1
			fi
			echo $b_new, "ds_config_zero${o}_offload.json", $model_name
			deepspeed --include="localhost:1" /home/yubo/GPU_training/transformers/examples/pytorch/translation/run_translation.py --deepspeed "ds_config_zero${o}_offload.json"  --model_name_or_path $model_name --per_device_train_batch_size $b --output_dir output_dir --overwrite_output_dir --fp16 --do_train --max_train_samples 500 --num_train_epochs $b_new --dataset_name wmt16 --dataset_config "ro-en" --source_lang en --target_lang ro >> "${b}_${o}_${model_name}_offload.txt"
			sleep 20
			kill -9 $pid
		done
	done
	
done
