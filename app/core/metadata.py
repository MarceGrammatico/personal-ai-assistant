from datetime import UTC, datetime

APP_BUILD_DATE = datetime.now(UTC)


def get_application_metadata() -> dict:
    """
    Returns application metadata.
    """

    return {
        "name": "Personal AI Assistant",
        "version": "0.1.0",
        "build_date": APP_BUILD_DATE,
    }
