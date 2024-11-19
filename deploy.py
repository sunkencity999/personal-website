import os
import ftplib
from pathlib import Path

# FTP Configuration
FTP_HOST = "ftp.christopherdanielbradford.com"
FTP_USER = "admin@christopherdanielbradford.com"
FTP_PASS = "CStyle32!"
FTP_PORT = 21

# Local directory configuration
LOCAL_DIR = Path(__file__).parent / "src"
REMOTE_ROOT = "public_html"  # Remote root directory

def upload_file(ftp, local_path, remote_path):
    """Upload a single file to FTP server"""
    with open(local_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_path}', file)
    print(f"Uploaded: {remote_path}")

def create_remote_dir(ftp, remote_dir):
    """Create remote directory if it doesn't exist"""
    try:
        ftp.mkd(remote_dir)
    except:
        pass  # Directory might already exist

def deploy():
    """Deploy the website via FTP"""
    try:
        # Connect to FTP server
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        print("Connected to FTP server")

        # Ensure public_html directory exists
        create_remote_dir(ftp, REMOTE_ROOT)

        # Walk through local directory
        for root, dirs, files in os.walk(LOCAL_DIR):
            # Calculate the remote directory path
            local_root = Path(root)
            relative_path = str(local_root.relative_to(LOCAL_DIR)).replace("\\", "/")
            if relative_path == ".":
                relative_path = ""
            
            remote_root = f"{REMOTE_ROOT}/{relative_path}".rstrip("/")

            # Create remote directories
            for dir_name in dirs:
                remote_dir = f"{remote_root}/{dir_name}"
                create_remote_dir(ftp, remote_dir)

            # Upload files
            for file_name in files:
                local_path = local_root / file_name
                remote_path = f"{remote_root}/{file_name}"
                upload_file(ftp, local_path, remote_path)

        print("Deployment completed successfully!")
        ftp.quit()

    except Exception as e:
        print(f"Error during deployment: {str(e)}")

if __name__ == "__main__":
    deploy()
