from src.crew.memory import save_to_memory, search_memory, get_memory_stats

print("=== Testing Memory ===\n")

# Save a fake incident
save_to_memory(
    container_name="test-nginx",
    logs="Error: port 80 already in use. Address already bound.",
    diagnosis="Port 80 is already occupied by another process.",
    fix="Restart the container. If recurring, check for port conflicts."
)

print("\n=== Memory Stats ===")
print(get_memory_stats())

print("\n=== Searching for similar incident ===")
result = search_memory(
    container_name="test-nginx",
    logs="Error: port 80 already in use. Cannot bind to address."
)

if result:
    print(f"Found match: {result['fix']}")
else:
    print("No match found")
