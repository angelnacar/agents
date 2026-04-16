from mcp.server.fastmcp import FastMCP

@mcp.tool()
async def get_jira_issue(issue_id: str) -> dict:
    jira_env = {"JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN")}
    jira_username = {"JIRA_USERNAME": os.getenv("JIRA_USERNAME")}
    """Obtiene los detalles de un issue de Jira.

    Args:
        issue_id: El ID del issue en Jira
    """
    # Aquí iría la lógica para conectarse a Jira y obtener los detalles del issue
     mcp_params = {
        "command": "uvx",
        "args": ["mcp-atlassian"],
        "env": {
                "JIRA_URL": "https://giss.atlassian.net",
                "JIRA_USERNAME": jira_username["JIRA_USERNAME"],
                "JIRA_API_TOKEN": jira_env["JIRA_API_TOKEN"]
                }
            }
    return mcp.run(mcp_params)
       

    }