import os
import multiprocessing


def replace(content: str, app_name: str, new_name: str):
    """Helper function to replace the app_name with new_name in file content passed as strings.

    Args:
        content  (str): the content of a file.
        app_name (str): the current name of the app.
        new_name (str): the new name of the app.
    """
    content = content.replace(
        f"static '{app_name}",
        f"static '{new_name}"
    ).replace(
        f"extends '{app_name}/",
        f"extends '{new_name}/"
    ).replace(
        f"include '{app_name}/",
        f"include '{new_name}/"
    ).replace(
        f"url '{app_name}:",
        f"url '{new_name}:"
    ).replace(
        f"translate '{app_name}'",
        f"translate '{new_name.capitalize()}'"
    )
    return content


def update_templates(app_name: str, new_name: str):
    """Update the templates and static files to reflect the change.

    Args:
        app_name (str): the current name of the app.
        new_name (str): the new name of the app.
    """
    path_to_templates = app_name + '/templates/' + app_name + '/'
    folders = os.listdir(path_to_templates)
    for sub_folder in folders:
        path_to_folder = path_to_templates + sub_folder + '/'
        for file in os.listdir(path_to_folder):
            if os.path.isdir(path_to_folder + file):
                for item in os.listdir(path_to_folder + file):
                    path_to_item = path_to_folder + file + '/' + item
                    content = open(path_to_item).read()
                    content = replace(content, app_name, new_name)
                    new_file = open(path_to_item, 'w')
                    new_file.write(content)
                    new_file.close()
            else:
                content = open(path_to_folder + file).read()
                content = replace(content, app_name, new_name)
                new_file = open(path_to_folder + file, 'w')
                new_file.write(content)
                new_file.close()
    os.rename(
        app_name + '/templates/' + app_name,
        app_name + '/templates/' + new_name
    )
    os.rename(
        app_name + '/static/' + app_name,
        app_name + '/static/' + new_name
    )


def update_imports(app_name: str, new_name: str):
    """Fix the imports in the views and forms

    Args:
        app_name (str): the current name of the app.
        new_name (str): the new name of the app.
    """
    folders = ['forms', 'views']
    for folder in folders:
        for file in os.listdir(app_name + '/' + folder):
            if file == '__pycache__':
                continue
            content = open(app_name + '/' + folder + '/' + file).read()
            content = content.replace(
                f'from {app_name}',
                f'from {new_name}'
            ).replace(
                f"app_name = '{app_name}'",
                f"app_name = '{new_name}'"
            ).replace(
                f"template_name = '{app_name}/",
                f"template_name = '{new_name}/"
            ).replace(
                f"reverse_lazy('{app_name}:",
                f"reverse_lazy('{new_name}:"
            )
            new_file = open(app_name + '/' + folder + '/' + file, 'w')
            new_file.write(content)
            new_file.close()


def update_urls(app_name: str, new_name: str):
    """Update the urls.py file to reflect the changes.

    Args:
        app_name (str): the current name of the app.
        new_name (str): the new name of the app.
    """
    file_path = app_name + '/urls.py'
    content = open(file_path).read()
    content = content.replace(
        f'from {app_name}',
        f'from {new_name}'
    ).replace(
        f"app_name = '{app_name}'",
        f"app_name = '{new_name}'"
    ).replace(
        f"template_name='{app_name}/",
        f"template_name='{new_name}/"
    ).replace(
        f"reverse_lazy('{app_name}:",
        f"reverse_lazy('{new_name}:"
    )
    new_file = open(file_path, 'w')
    new_file.write(content)
    new_file.close()


def update_models(app_name: str, new_name: str):
    """Update the models.py file to reflect the changes.

    Args:
        app_name (str): the current name of the app.
        new_name (str): the new name of the app.
    """
    file_path = app_name + '/models.py'
    content = open(file_path).read()
    content = content.replace(
        f"reverse_lazy('{app_name}:' + suffix + '_list')",
        f"reverse_lazy('{new_name}:' + suffix + '_list')"
    )
    new_file = open(file_path, 'w')
    new_file.write(content)
    new_file.close()


def update_migrations(app_name: str, new_name: str):
    folder = app_name + '/migrations/'
    for file in os.listdir(folder):
        if file == '__pycache__':
            continue
        content = open(folder + file).read()
        content = content.replace(
            f"import {app_name}",
            f"import {new_name}"
        ).replace(
            f'bases=({app_name}',
            f'bases=({new_name}'
        )
        new_file = open(folder + file, 'w')
        new_file.write(content)
        new_file.close()


def rename_package(app_name: str, new_name: str):
    """Rename the app package to be the new name.

    Args:
        app_name (str): the current name of the app.
        new_name (str): the new name of the app.
    """
    os.rename(app_name, new_name)


def rename_apps(app_name: str, new_name: str):
    """Change the name of Configuration class and the name attribute to the new name

    Args:
        app_name (str): the current name of the app.
        new_name (str): the new name of the app.
    """
    content = open(app_name + '/apps.py').read()
    replaced_name = app_name.capitalize() if app_name != 'JApp' else app_name
    content = content.replace(
        f'{replaced_name}Config',
        f'{new_name.capitalize()}Config'
    ).replace(
        f"name = '{app_name}'",
        f"name = '{new_name.lower()}'"
    )
    file = open(app_name + '/apps.py', 'w')
    file.write(content)
    file.close()


processes = [
    update_imports,
    update_models,
    update_migrations,
    update_urls,
    update_templates,
    rename_apps,
    rename_package,
]


def run(app_name='JApp', new_name='test'):
    for process in processes:
        p = multiprocessing.Process(process(app_name, new_name))
        p.start()
