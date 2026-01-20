from typing import List


def load_hosts_from_file(filepath: str) -> List[str]:
    try:
        with open(filepath, 'r') as f:
            hosts = [line.strip() for line in f if line.strip()]
        
        if not hosts:
            raise ValueError("File is empty or contains no valid hosts")
        
        return hosts
    except FileNotFoundError:
        raise ValueError(f"File not found: {filepath}")
    except IOError as e:
        raise ValueError(f"Error reading file: {e}")


def save_output(content: str, filepath: str) -> None:
    try:
        with open(filepath, 'w') as f:
            f.write(content)
    except IOError as e:
        raise ValueError(f"Error writing output file: {e}")