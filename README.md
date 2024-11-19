# Kaggle Script Action

**Kaggle Script Action** automates running model training and CI/CD workflows on Kaggle kernels for machine learning workflows in your GitHub repo. 
<br>
It pulls the current branch, installs dependencies from the working subdirectory `requirements.txt` by default, and supports running Python scripts with options like GPU/TPU, internet access, and custom dataset dependencies.

## Key Features
- **Automated Kernel Execution**: Run Python scripts on Kaggle kernels from GitHub Actions, with options for enabling free GPU, TPU, and internet.
- **Flexible Configuration**: Specify kernel parameters like title, custom script, data sources, and sleep intervals for status checks.
- **Dynamic Script Injection**: Accepts a custom script input that is added directly to the Kaggle notebook, making it versatile for various tests and jobs.
- **CI/CD Integration**: Incorporate machine learning workflows seamlessly into your CI/CD pipeline, with GitHub Actions monitoring the kernel execution status and fetching output logs.
- **Detailed Logging**: Captures and logs the complete output, including kernel execution logs and errors, and displays `data` fields for streamlined debugging.
  
## Usage
Sign up for a [Kaggle Account](https://www.kaggle.com/account/login?phase=startRegisterTab) and verify the account.
Go to your account page, then settings. Create your API Token. You'll get a file with something like this:
```json
{
  "username": "USERNAME",
  "key": "TOKEN"
}
```
Add `USERNAME` and `TOKEN` to Github Actions Secrets as `KAGGLE_USERNAME` and `KAGGLE_KEY`.

## Inputs
| Parameter            | Requirement | Description                                                                                                                                                                                                                      | Default Value                                                                                                                                                                 |
|----------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`           | Required    | Kaggle username.                                                                                                                                                                                                                | N/A                                                                                                                                                                           |
| `key`                | Required    | Kaggle API token.                                                                                                                                                                                                               | N/A                                                                                                                                                                           |
| `title`              | Required    | Title of execution run.                                                                                                                                                                                                         | N/A                                                                                                                                                                           |
| `working_subdir`     | Optional    | Subdirectory inside `/kaggle/working/REPO_NAME` where dependencies are installed and the custom script is run.                                                                                                                  | `""` <br>(this executes inside `/kaggle/working/REPO_NAME`) <br><br> Example <br><br> Set `working_subdir: "src"` to execute commands inside `/kaggle/working/REPO_NAME/src`. |
| `custom_script`      | Required    | Custom script content to execute within the notebook.                                                                                                                                                                           | `print('Success')`                                                                                                                                                            |
| `enable_gpu`         | Optional    | Enable GPU on the Kaggle kernel.                                                                                                                                                                                                | `false`                                                                                                                                                                       |
| `enable_tpu`         | Optional    | Enable TPU on the Kaggle kernel.                                                                                                                                                                                                | `false`                                                                                                                                                                       |
| `enable_internet`    | Optional    | Enable internet access for the Kaggle kernel.                                                                                                                                                                                   | `true`                                                                                                                                                                        |
| `dataset_sources`    | Optional    | List of dataset sources formatted as `{username}/{dataset-slug}`.                                                                                                                                                               | N/A                                                                                                                                                                           |
| `competition_sources`| Optional    | List of competition data sources.                                                                                                                                                                                               | N/A                                                                                                                                                                           |
| `kernel_sources`     | Optional    | List of other kernel sources formatted as `{username}/{kernel-slug}`.                                                                                                                                                           | N/A                                                                                                                                                                           |
| `sleep_time`         | Optional    | Time interval (in seconds) to wait between kernel status checks.                                                                                                                                                                | `15`                                                                                                                                                                          |



## Example Usage(Running unittests)

```yaml
name: Run Tests on Pull Request

on:
  pull_request:

jobs:
  run_unit_tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Execute Kaggle Script Action
        uses: KevKibe/kaggle-script-action@v1.0.5
        with:
          username: ${{ secrets.KAGGLE_USERNAME }}
          key: ${{ secrets.KAGGLE_KEY }}
          title: "Run Unit Tests"
          custom_script: |
                pytest test.py
          enable_internet: true
          enable_gpu: false
          enable_tpu: false
          sleep_time: 10
```
## Example Usage(Training a Bert Model)
```yaml
name: Train Bert Model on Push to Main

on:
  push:
    branches:
      - main

jobs:
  run_model_training:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Run Bert Model Training
        uses: KevKibe/kaggle-script-action@v1.0.5
        with:
          username: ${{ secrets.KAGGLE_USERNAME }}
          key: ${{ secrets.KAGGLE_KEY }}
          title: "Run Bert Model Training"
          custom_script: |
                python train.py --model-name bert-base-uncased \
                                        --train-file data/train.csv \
                                        --validation-file data/val.csv \
                                        --output-dir models/bert-text-classifier \
                                        --batch-size 16 \
                                        --learning-rate 3e-5 \
                                        --num-epochs 3 \
                                        --max-seq-length 128
          enable_internet: true
          enable_gpu: true
          enable_tpu: false
          sleep_time: 60
```
<br>

`train.py`
```python
import argparse
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer
from datasets import load_dataset

def main(args):
    # Load dataset
    dataset = load_dataset('csv', data_files={'train': args.train_file, 'validation': args.validation_file})

    # Load model and tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(args.model_name)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    # Tokenize data
    def preprocess(examples):
        return tokenizer(examples['text'], truncation=True, max_length=args.max_seq_length)
    tokenized_dataset = dataset.map(preprocess, batched=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        evaluation_strategy="epoch"
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset['validation']
    )

    # Train
    trainer.train()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a Hugging Face Transformer model for text classification.")
    parser.add_argument("--model-name", type=str, required=True, help="Name of the model to load from Hugging Face.")
    parser.add_argument("--train-file", type=str, required=True, help="Path to the training data file.")
    parser.add_argument("--validation-file", type=str, required=True, help="Path to the validation data file.")
    parser.add_argument("--output-dir", type=str, required=True, help="Directory to save the model.")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size for training.")
    parser.add_argument("--learning-rate", type=float, default=3e-5, help="Learning rate.")
    parser.add_argument("--num-epochs", type=int, default=3, help="Number of epochs.")
    parser.add_argument("--max-seq-length", type=int, default=128, help="Maximum sequence length for tokenization.")

    args = parser.parse_args()
    main(args)
```



**Note**: To use this action, you must have a Kaggle API token with the appropriate permissions for kernels and datasets.
