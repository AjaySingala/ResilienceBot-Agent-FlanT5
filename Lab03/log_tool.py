# Import the Tool Decorator
from langchain_core.tools import tool

LOG_FILE = "logs/system_logs.txt"

@tool
def log_search(query: str) -> str:
        # Tool Description.
    """
    Search system logs for error spikes and operational events.
    """

    # Read the Log File.
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    # Initialize Data Structures.
    errors = []
    services = {}

    # Process Each Log Line.
    for line in logs:
            # Detect Errors.
        if "ERROR" in line:
                # Store Error Lines.
            errors.append(line.strip())

            # Count Errors by Service.
            if "Payment" in line:
                services["payment"] = services.get("payment", 0) + 1

            if "Redis" in line or "Login" in line:
                services["login"] = services.get("login", 0) + 1

            if "DB" in line or "Checkout" in line:
                services["checkout"] = services.get("checkout", 0) + 1

    # Decide What to Return.
    if "spike" in query.lower() or "error" in query.lower():
        # Create the Summary.
        summary = []
        for s, count in services.items():
            summary.append(f"{s} service had {count} errors")
        
        # Combine summary lines and return.
        return "\n".join(summary)

    # Otherwise Return Raw Logs.
    return "\n".join(errors[:5])
