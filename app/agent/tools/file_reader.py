def read_file(path: str) -> str:
    try:
        return open(path, "r").read()
    except:
        return ""
