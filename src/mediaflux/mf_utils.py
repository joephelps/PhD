import subprocess
import os
from pathlib import Path

def connect_to_mediaflux(profile="default"):
    print(f"Connecting to Mediaflux with profile: {profile}")

def upload_to_mediaflux(local_path, dest_path, profile=None):
    """
    Upload a file or folder to Mediaflux.

    Parameters
    ----------
    local_path : str or Path
        Path to the local file or directory you want to upload.
    dest_path : str
        Destination path in Mediaflux, e.g. '/projects/proj-myproject-1234/data'.
    profile : str, optional
        Mediaflux profile to use (e.g. 'default'). If None, uses the default profile.
    """
    local_path = Path(local_path).expanduser().resolve()
    if not local_path.exists():
        raise FileNotFoundError(f"Local path not found: {local_path}")

    cmd = ["unimelb-mf-upload", "--dest", dest_path, str(local_path)]
    if profile:
        cmd.extend(["--profile", profile])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Upload failed:\n{result.stderr}")

    print(f"Upload successful: {local_path} > {dest_path}")


def download_from_mediaflux(src_path, local_dir=".", profile=None):
    """
    Download a file or folder from Mediaflux.

    Parameters
    ----------
    src_path : str
        Path in Mediaflux to download, e.g. '/projects/proj-myproject-1234/data/myfile.csv'.
    local_dir : str or Path, optional
        Local directory to save the downloaded file(s). Defaults to current working directory.
    profile : str, optional
        Mediaflux profile to use. If None, uses the default profile.

    Returns
    -------
    str : path to the downloaded file or directory
    """
    local_dir = Path(local_dir).expanduser().resolve()
    os.makedirs(local_dir, exist_ok=True)

    cmd = ["unimelb-mf-download", "--src", src_path, str(local_dir)]
    if profile:
        cmd.extend(["--profile", profile])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Download failed:\n{result.stderr}")

    print(f"Download successful: {src_path} > {local_dir}")
    return str(local_dir)
