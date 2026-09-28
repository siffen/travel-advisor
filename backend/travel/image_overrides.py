"""Optional per-destination image overrides.

Add an exact destination key here when you want to replace the automatically
resolved image. Key format is: country|state|city|name (lowercase).
"""

IMAGE_OVERRIDES: dict[str, str] = {
    # Example:
    # "india|madhya pradesh|bhopal|bhopal": "https://example.com/bhopal.jpg",
}
