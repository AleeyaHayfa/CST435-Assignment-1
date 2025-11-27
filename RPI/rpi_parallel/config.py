import os

# Detect if running inside Docker
IN_DOCKER = os.getenv("DOCKER", "0") == "1"

if IN_DOCKER:
    # Docker environment: container names + internal ports
    SERVICES = [
        ("service_a", 9000),
        ("service_b", 9001),
        ("service_c", 9002),
        ("service_d", 9003),
        ("service_e", 9004)
    ]
else:
    # Localhost: different ports for each service
    SERVICES = [
        ("localhost", 9010),
        ("localhost", 9011),
        ("localhost", 9012),
        ("localhost", 9013),
        ("localhost", 9014)
    ]
