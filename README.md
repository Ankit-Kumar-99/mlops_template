### Step 1: Install Cookiecutter
First, make sure Cookiecutter is installed. Open your terminal and run the following command to install it via pip:

```sh
pip install cookiecutter==2.6.0
```
### Step 2: Obtain the Template
Ensure you have access to the Cookiecutter template directory. You should either have the template directory on your local machine or have a URL where you can access it.

### Step 3: Generate Your Project
Navigate to the parent directory where you want to create your new project. Use the following command to generate the project from the template. Replace /path/to/cookiecutter-template with the path to your template directory or the URL if using an online repository:

``` sh
cookiecutter /path/to/cookiecutter-template
```
### Step 4: Select the Template
During the generation process, you will be prompted to select from the available templates: the Starter template or the Time Series template. This option ensures you have the correct project setup based on your requirements.

### Step 5: Enter the Required Values
After selecting the template, you will be prompted to provide several values to configure your project. The required values include:

- **project_name:**  Enter the name of your project.
- **existing_cluster_id:** Enter the ID of the existing cluster.
- **host:** Enter the host information.

For example:

```sh
project_name [enter name]: my_project
existing_cluster_id [enter cluster id]: cluster_123
host [enter host]: my_host.example.com
```
### Step 6: Verify Project Creation
Once you've provided the necessary values, Cookiecutter will generate a new project directory with the specified project_name. Check the generated directory to ensure it matches your specifications and contains the expected files and structure.

### Example Walkthrough
Here's an example of the entire process:

1. Install Cookiecutter:
```sh
pip install cookiecutter
```
2. Navigate to the desired parent directory:
``` sh
cd /path/to/parent-directory
```
3. Generate the project from the template:
``` sh
cookiecutter /path/to/cookiecutter-template
```
4. Select the template and enter the required values when prompted:
``` less
Select template:
1 - Starter template
2 - Time Series template
Choose from 1 or 2 [1]: 1

project_name [enter name]: my_project
existing_cluster_id [enter cluster id]: cluster_123
host [enter host]: my_host.example.com
```
5. Verify the created project directory:
```sh
cd my_project
ls
```
Check the structure and contents of the generated project directory to ensure everything is set up as expected.