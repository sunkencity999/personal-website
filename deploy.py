import os
import ftplib
from pathlib import Path
import sys

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
    try:
        with open(local_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_path}', file)
        print(f"Uploaded: {remote_path}")
        return True
    except Exception as e:
        print(f"Error uploading {local_path}: {str(e)}")
        return False

def create_remote_dir(ftp, remote_dir):
    """Create remote directory if it doesn't exist"""
    try:
        current = ftp.pwd()
        # Split the path and create each directory in sequence
        parts = remote_dir.split('/')
        for part in parts:
            if not part:
                continue
            try:
                ftp.cwd(part)
            except:
                try:
                    ftp.mkd(part)
                    ftp.cwd(part)
                except Exception as e:
                    print(f"Warning: Could not create/access directory {part}: {str(e)}")
                    ftp.cwd(current)
                    return False
        ftp.cwd(current)
        return True
    except Exception as e:
        print(f"Error creating directory structure {remote_dir}: {str(e)}")
        return False

def deploy():
    """Deploy the website via FTP"""
    try:
        # Connect to FTP server
        print(f"Connecting to {FTP_HOST}...")
        ftp = ftplib.FTP()
        ftp.set_debuglevel(2)  # Enable debugging
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        print("Connected to FTP server")

        # Create base directories first
        base_dirs = [
            REMOTE_ROOT,
            f"{REMOTE_ROOT}/css",
            f"{REMOTE_ROOT}/fonts",
            f"{REMOTE_ROOT}/fonts/regular",
            f"{REMOTE_ROOT}/fonts/italic",
            f"{REMOTE_ROOT}/fonts/bold"
        ]
        
        for remote_dir in base_dirs:
            if not create_remote_dir(ftp, remote_dir):
                print(f"Failed to create directory structure: {remote_dir}")
                continue

        # Walk through the local directory
        success_count = 0
        error_count = 0
        
        for root, dirs, files in os.walk(LOCAL_DIR):
            # Calculate the relative path from LOCAL_DIR
            rel_path = os.path.relpath(root, LOCAL_DIR)
            if rel_path == '.':
                remote_root = REMOTE_ROOT
            else:
                remote_root = os.path.join(REMOTE_ROOT, rel_path).replace('\\', '/')
            
            # Upload each file
            for file in files:
                local_path = os.path.join(root, file)
                remote_path = f"{remote_root}/{file}".replace('\\', '/')
                
                if upload_file(ftp, local_path, remote_path):
                    success_count += 1
                else:
                    error_count += 1

        print(f"\nDeployment Summary:")
        print(f"Successfully uploaded: {success_count} files")
        print(f"Failed to upload: {error_count} files")
        
        if error_count == 0:
            print("\nDeployment completed successfully!")
            return 0
        else:
            print("\nDeployment completed with errors.")
            return 1
    
    except Exception as e:
        print(f"Deployment failed: {str(e)}")
        return 1
    finally:
        try:
            ftp.quit()
        except:
            pass

if __name__ == "__main__":
    sys.exit(deploy())
