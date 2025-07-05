# Dummy admin logic for now
async def get_current_admin():
    # TODO: Implement admin RBAC
    return "admin@example.com"

async def get_stats(user_email):
    # TODO: Aggregate stats from DBs
    return {
        "users": 10,
        "documents": 25,
        "queries": 100
    }
