from googleapiclient import discovery

def create_instance(compute, project, config):
    name = config["name"]
    zone = config["zone"]
    machine_type = f"zones/{zone}/machineTypes/{config['machine_type']}"
    image_response = compute.images().getFromFamily(
        project=config["image_project"], family=config["image_family"]).execute()
    source_disk_image = image_response["selfLink"]

    config_body = {
        "name": name,
        "machineType": machine_type,
        "disks": [{
            "boot": True,
            "autoDelete": True,
            "initializeParams": {
                "sourceImage": source_disk_image,
            }
        }],
        "networkInterfaces": [{
            "network": "global/networks/default",
            "accessConfigs": [{"type": "ONE_TO_ONE_NAT", "name": "External NAT"}]
        }],
    }

    return compute.instances().insert(project=project, zone=zone, body=config_body).execute()
