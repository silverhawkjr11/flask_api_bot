import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

TEMPLATES = {
    'app.py': 'app.py.template',
    'config/config.py': 'config/config.py.template',
    'utils/encoder.py': 'utils/encoder.py.template',
    'utils/functions.py': 'utils/functions.py.template',
    'utils/variables.py': 'utils/variables.py.template',
    'routes/auth.py': 'routes/auth.py.template',
    'middlewares/jwt_class.py': 'middlewares/jwt_class.py.template',
    'routes/empty_route.py': 'routes/empty_route.py.template',
}

def create_project_structure(project_name):
    os.makedirs(f"{project_name}/config", exist_ok=True)
    os.makedirs(f"{project_name}/utils", exist_ok=True)
    os.makedirs(f"{project_name}/routes", exist_ok=True)
    os.makedirs(f"{project_name}/middlewares", exist_ok=True)

def render_template(env, template_path, context):
    try:
        template = env.get_template(template_path)
        return template.render(context)
    except TemplateNotFound:
        print(f"Template not found: {template_path}")
        raise

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def generate_project(project_name, config, routes):
    create_project_structure(project_name)
    context = {'g_jwt_algorithm': config['g_jwt_algorithm'],
               'g_jwt_secret': config['g_jwt_secret'],
               'g_online': config['g_online'],
               'g_jwt_expiration_time': config['g_jwt_expiration_time'],
               'g_host': config['g_host'],
               'g_port': config['g_port'],
               'g_is_debug': config['g_is_debug'],
               'g_users': config['g_users'],
               'routes': routes}

    env = Environment(loader=FileSystemLoader('templates'))

    for file_path, template_path in TEMPLATES.items():
        if template_path:
            content = render_template(env, template_path, context)
        else:
            content = ''
        write_file(f"{project_name}/{file_path}", content)

    for route in routes:
        print(f"Generating route '{route}'")
        content = render_template(env, 'routes/empty_route.py.template', {'route_name': route.strip()})
        write_file(f"{project_name}/routes/{route.strip()}.py", content)

if __name__ == "__main__":
    project_name = input("Enter the project name: ")

    config = {
        'g_jwt_algorithm': input("Enter JWT algorithm (default 'HS256'): ") or 'HS256',
        'g_jwt_secret': input("Enter JWT secret: ") or "123",
        'g_online': input("Is the app online? (True/False): ") or False,
        'g_jwt_expiration_time': int(input("Enter JWT expiration time (in minutes, default 30): ") or 30),
        'g_host': input("Enter host (default '0.0.0.0'): ") or '0.0.0.0',
        'g_port': int(input("Enter port (default 4000): ") or 4000),
        'g_is_debug': input("Is debug mode on? (True/False): ") or True,
        'g_users': {}
    }

    num_users = int(input("Enter number of users: "))
    for i in range(num_users):
        user_id = input(f"Enter user ID {i+1}: ")
        users = []
        while True:
            username = input("Enter username (or leave blank to finish): ")
            if not username:
                break
            password = input("Enter password: ")
            users.append({'username': username, 'password': password})
        config['g_users'][user_id] = users

    routes_input = input("Enter route names separated by commas (excluding 'auth'): ")
    routes = [route.strip() for route in routes_input.split(',') if route.strip()]

    generate_project(project_name, config, routes)
    print(f"Project '{project_name}' generated successfully.")
