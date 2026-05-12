from src.crew.tools import (
    list_containers,
    detect_failed_containers,
)

print("=== Testing list_containers ===")
print(list_containers.run("check"))

print("\n=== Testing detect_failed_containers ===")
print(detect_failed_containers.run("check"))
