import yaml
import glob

def read_requirements(file_path):
    """
    Read and return the list of requirements from a file.

    This function reads the specified requirements file, stripping out any empty lines
    and comments, and returns the remaining lines as a list.

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        list: A list of requirement strings.

    Example:
        requirements = read_requirements('requirements.txt')
        print(requirements)
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

def update_libraries_section(yaml_data, requirements):
    """
    Update the 'libraries' section in the YAML data with the given requirements.

    This function creates a list of library definitions from the requirements and updates
    the 'libraries' section in the YAML data for each task.

    Args:
        yaml_data (dict): The YAML data to update.
        requirements (list): A list of requirement strings.

    Example:
        yaml_data = {
            'tasks': [
                {'name': 'task1', 'libraries': []},
                {'name': 'task2', 'libraries': []}
            ]
        }
        update_libraries_section(yaml_data, ['numpy', 'pandas'])
        print(yaml_data)
    """
    library_list = []
    for req in requirements:
        if req.startswith('/Volumes'):
            library_list.append({'whl': req})
        else:
            library_list.append({'pypi': {'package': req}})
    
    def update_task_libraries(task):
    # Check if the task is a notebook_task or spark_python_task
        if 'notebook_task' in task or 'spark_python_task' in task:
            task['libraries'] = library_list
       
         # Check if the task is a for_each_task, and recursively update its sub-task
        elif 'for_each_task' in task:
            # Get inside the 'task' key within 'for_each_task'
            sub_task = task['for_each_task'].get('task')
            if sub_task:
                sub_task['libraries'] = library_list
 

    def traverse_and_update(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == 'tasks' and isinstance(value, list):
                    for task in value:
                        update_task_libraries(task)
                traverse_and_update(value)
        elif isinstance(node, list):
            for item in node:
                traverse_and_update(item)

    traverse_and_update(yaml_data)

def update_yaml_libraries(yaml_file_path, requirements):
    """
    Update the 'libraries' section of a YAML file with the given requirements.

    This function reads a YAML file, updates its 'libraries' section with the requirements,
    and writes the updated data back to the file.

    Args:
        yaml_file_path (str): The path to the YAML file.
        requirements (list): A list of requirement strings.

    Example:
        update_yaml_libraries('resources/task.yml', ['numpy', 'pandas'])
    """
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    update_libraries_section(data, requirements)

    with open(yaml_file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=True, sort_keys=False)

requirements = read_requirements('requirements.txt')
yaml_files = glob.glob('resources/**/*.yml')

for yaml_file in yaml_files:
    update_yaml_libraries(yaml_file, requirements)
