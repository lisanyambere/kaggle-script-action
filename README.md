### Kaggle Script Action

**Kaggle Script Action** is a GitHub Action designed for automating the execution of custom scripts on Kaggle kernels, making it ideal for continuous integration (CI) and deployment (CD) of machine learning workflows directly within your GitHub repository. 
<br>
This action pulls the repository on the branch it is executed from, installs dependencies from the `requirements.txt` file in the root directory by default, and supports executing Python scripts on Kaggle's infrastructure with configurable options, including GPU/TPU support, internet access, and custom dataset or kernel dependencies. 

#### Key Features
- **Automated Kernel Execution**: Run Python scripts on Kaggle kernels from GitHub Actions, with options for enabling GPU, TPU, and internet.
- **Flexible Configuration**: Specify kernel parameters like title, custom script, data sources, and sleep intervals for status checks.
- **Dynamic Script Injection**: Accepts a custom script input that is added directly to the Kaggle notebook, making it versatile for various tests and jobs.
- **CI/CD Integration**: Incorporate machine learning workflows seamlessly into your CI/CD pipeline, with GitHub Actions monitoring the kernel execution status and fetching output logs.
- **Detailed Logging**: Captures and logs the complete output, including kernel execution logs and errors, and displays `data` fields for streamlined debugging.
  
#### Usage
Sign up for a [Kaggle Account](https://www.kaggle.com/account/login?phase=startRegisterTab) and verify the account.
Go to your account page, then settings. Create your API Token. You'll get a file with something like this:
```json
{
  "username": "USERNAME",
  "key": "TOKEN"
}
```
Add `USERNAME` and `TOKEN` to Github Actions Secrets as `KAGGLE_USERNAME` and `KAGGLE_KEY`.

#### Inputs
- **`username`** (required): Kaggle username.
- **`key`** (required): Kaggle API token.
- **`title`** (required): Title of execution run.
- **`custom_script`** (required): Custom script content to execute within the notebook. Default: `print('Success')`.
- **`enable_gpu`** (optional): Enable GPU on the Kaggle kernel. Default: `false`.
- **`enable_tpu`** (optional): Enable TPU on the Kaggle kernel. Default: `false`.
- **`enable_internet`** (optional): Enable internet access for the Kaggle kernel. Default: `true`.
- **`dataset_sources`** (optional): List of dataset sources formatted as `{username}/{dataset-slug}`.
- **`competition_sources`** (optional): List of competition data sources.
- **`kernel_sources`** (optional): List of other kernel sources formatted as `{username}/{kernel-slug}`.
- **`sleep_time`** (optional): Time interval (in seconds) to wait between kernel status checks. Default: `15`.


#### Example Usage
```yaml
name: Run Tests

on: [pull_request]

jobs:
  test_kaggle_action:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Run Kaggle Action
        uses: Kev
        with:
          username: ${{ secrets.KAGGLE_USERNAME }}
          key: ${{ secrets.KAGGLE_KEY }}
          title: "Kernel Test v2"
          custom_script: "pytest tests/test.py"
          enable_internet: true
          enable_gpu: false
          enable_tpu: false
          sleep_time: 10
```

**Note**: To use this action, you must have a Kaggle API token with the appropriate permissions for kernels and datasets.