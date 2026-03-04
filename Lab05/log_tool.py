from langchain_core.tools import tool

LOG_FILE = "logs/system_logs.txt"

@tool
def log_search(query: str) -> str:
    """
    Search system logs for error spikes and operational events.
    """

    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    errors = []
    services = {}

    for line in logs:

        if "ERROR" in line:

            errors.append(line.strip())

            if "Payment" in line:
                services["payment"] = services.get("payment", 0) + 1

            if "Redis" in line or "Login" in line:
                services["login"] = services.get("login", 0) + 1

            if "DB" in line or "Checkout" in line:
                services["checkout"] = services.get("checkout", 0) + 1

    if "spike" in query.lower() or "error" in query.lower():

        summary = []

        for s, count in services.items():
            summary.append(f"{s} service had {count} errors")

        return "\n".join(summary)

    return "\n".join(errors[:5])
