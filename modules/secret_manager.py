from google.cloud import secretmanager
from google.api_core.exceptions import AlreadyExists

def create_secret(client, secret_id: str, project_id: str):
    parent = f"projects/{project_id}"

    try:
        client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {
                    "replication": {"automatic": {}}
                }
            }
        )
        print(f"Secret creado: {secret_id}")
    except AlreadyExists:
        print(f"El secreto ya existe: {secret_id}")
    except Exception as e:
        print(f"Error creando {secret_id}: {e}")

def create_project_secrets(client_name: str, project_id: str, config: dict, env: str):
    client = secretmanager.SecretManagerServiceClient()

    service_name = config.get("secret_manager", {}).get("service_name")
    if not service_name:
        print("No se encontró 'service_name' en el config.")
        return

    secret_id = f"{service_name}-{client_name}-{env}"
    create_secret(client, secret_id, project_id)
