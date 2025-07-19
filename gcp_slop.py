import os
from google.cloud import compute_v1
from google.api_core.exceptions import GoogleAPICallError
import _KUNCI

PROJECT_ID = _KUNCI.PROJECT_ID
ZONE = _KUNCI.ZONE
INSTANCE_NAME = _KUNCI.INSTANCE_NAME


def start_vm() -> str:
    """Start a stopped Google Cloud VM instance."""
    try:
        client = compute_v1.InstancesClient()
        operation = client.start(
            project=PROJECT_ID,
            zone=ZONE,
            instance=INSTANCE_NAME
        )
        operation.result()
        return f"✅ Mesin {INSTANCE_NAME} geus hurung"
    except GoogleAPICallError as e:
        print(e.message)
        return f"❌ Teu bisa ngahirupkeun mesin: Parios dina konsol"


def stop_vm() -> str:
    """Stop a running Google Cloud VM instance."""
    try:
        client = compute_v1.InstancesClient()
        operation = client.stop(
            project=PROJECT_ID,
            zone=ZONE,
            instance=INSTANCE_NAME
        )
        operation.result()
        return f"🛑 Mesin {INSTANCE_NAME} geus dipareuman"
    except GoogleAPICallError as e:
        print(e.message)
        return f"❌ Teu bisa mareuman mesin: Parios dina konsol"


def restart_vm() -> str:
    """Restart a running Google Cloud VM instance."""
    try:
        client = compute_v1.InstancesClient()
        operation = client.reset(
            project=PROJECT_ID,
            zone=ZONE,
            instance=INSTANCE_NAME
        )
        operation.result()
        return f"🔄 Mesin {INSTANCE_NAME} geus di-restart"
    except GoogleAPICallError as e:
        print(e.message)
        return f"❌ Teu bisa ngarestart mesin: Parios dina konsol"


def get_vm_ip() -> str:
    """Get the external IP address of a VM instance."""
    try:
        client = compute_v1.InstancesClient()
        instance = client.get(
            project=PROJECT_ID,
            zone=ZONE,
            instance=INSTANCE_NAME
        )

        for interface in instance.network_interfaces:
            for config in interface.access_configs:
                if config.nat_i_p:
                    return config.nat_i_p
        return "Teu kapanggih IP na"
    except GoogleAPICallError as e:
        print(e.message)
        return f"❌ Gagal nyokot IP: Parios dina konsol"


def get_vm_status() -> str:
    """Get the current status of a VM instance."""
    try:
        client = compute_v1.InstancesClient()
        instance = client.get(
            project=PROJECT_ID,
            zone=ZONE,
            instance=INSTANCE_NAME
        )
        return instance.status
    except GoogleAPICallError as e:
        print(e.message)
        return "❌ Gagal ngacek status: Parios dina konsol"


def __menu():
    print(INSTANCE_NAME)
    """Interactive menu for VM management"""
    while True:
        print("\nGoogle Cloud VM Manager")
        print("1. Start VM")
        print("2. Stop VM")
        print("3. Restart VM")
        print("4. Check Status")
        print("5. Get IP Address")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            start_vm()
        elif choice == '2':
            stop_vm()
        elif choice == '3':
            restart_vm()
        elif choice == '4':
            status = get_vm_status()
            print(f"\nCurrent Status: {status}")
        elif choice == '5':
            ip = get_vm_ip()
            print(f"\nExternal IP: {ip}")
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    # Verify configuration
    required_vars = ['GCP_PROJECT_ID', 'GCP_ZONE', 'GCP_INSTANCE_NAME']
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print(f"⚠️ Missing environment variables: {', '.join(missing)}")
        print("Create a .env file with these variables")
    else:
        __menu()
