import yaml
from modules import secret_manager

def load_yaml(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    env = "develop"

    global_config = load_yaml("config/global.yaml")
    env_config = load_yaml(f"config/{env}.yaml")

    client_name = global_config["client_name"]
    project_id = global_config[f"project_id_{env}"]

    secret_manager.create_project_secrets(client_name, project_id, env_config, env)

if __name__ == "__main__":
    main()
