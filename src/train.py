import logging
import os
import sys
from typing import Tuple

import datasets
import transformers
from transformers import HfArgumentParser

from args import DataArguments, ExperimentalArguments, ModelArguments, TrainingArguments

logger = logging.getLogger(__name__)


def parse_args() -> (
    Tuple[
        ModelArguments,
        DataArguments,
        TrainingArguments,
        ExperimentalArguments,
    ]
):
    parser = HfArgumentParser(
        (ModelArguments, DataArguments, TrainingArguments, ExperimentalArguments)
    )

    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        (
            model_args,
            data_args,
            training_args,
            experimental_args,
        ) = parser.parse_json_file(json_file=os.path.abspath(sys.argv[1]))
    else:
        (
            model_args,
            data_args,
            training_args,
            experimental_args,
        ) = parser.parse_args_into_dataclasses()

    return model_args, data_args, training_args, experimental_args


def set_logger(log_level):
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Set logging level
    logger.setLevel(log_level)

    # Set logging level for datasets and transformers
    datasets.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.enable_default_handler()
    transformers.utils.logging.enable_explicit_format()


def main():
    model_args, data_args, training_args, experimental_args = parse_args()

    # Set logger
    log_level = training_args.get_process_log_level()
    set_logger(log_level)

    # Log arguments
    logger.warning(
        f"Process rank: {training_args.local_rank}, device: {training_args.device}, n_gpu: {training_args.n_gpu} "
        f"distributed training: {bool(training_args.local_rank != -1)}, 16-bits training: {training_args.fp16}"
    )
    logger.info(f"Training/evaluation parameters {training_args}")
