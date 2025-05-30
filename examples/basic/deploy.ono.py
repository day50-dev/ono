import os

# Get platform-appropriate paths
TEMP_DIR = "<?ono get users temp directory ?>"
CONFIG_DIR = "<?ono get users config directory ?>"
CURRENT_USER = "<?ono get current username ?>"

print(f"Temp directory: {TEMP_DIR}")
print(f"Config directory: {CONFIG_DIR}")
print(f"Current user: {CURRENT_USER}")

# Create a directory in the temp directory
os.makedirs(os.path.join(TEMP_DIR, "my_app"), exist_ok=True)