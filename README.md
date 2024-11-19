# Personal Website - Christopher Bradford

A modern, responsive personal website showcasing professional experience and skills.

## Features

- Modern, responsive design
- Interactive UI with smooth animations
- Mobile-friendly navigation
- Sections for About, Skills, Experience, and Contact
- Built with HTML5, TailwindCSS, and AlpineJS

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
python server.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Configuration

To deploy the website, you'll need to set up your FTP credentials:

1. Copy `config.ini.example` to `config.ini`
2. Edit `config.ini` with your FTP credentials:
   ```ini
   [FTP]
   host = your.ftp.host.com
   user = your_username
   password = your_password
   port = 21
   ```
3. The `config.ini` file is excluded from version control for security

## Deployment

To deploy the website to the production server:

1. Make sure all your changes are saved
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the deployment script:
   ```bash
   python deploy.py
   ```

The script will automatically upload all files from the `src` directory to the production server via FTP.

## Project Structure

```
personal-website/
├── src/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   ├── img/
│   └── index.html
├── server.py
├── deploy.py
├── requirements.txt
└── README.md
```

## Technologies Used

- HTML5
- TailwindCSS (for styling)
- AlpineJS (for interactivity)
- Flask (for local development server)

## Customization

- Edit `src/index.html` to modify content
- Update `src/css/styles.css` for custom styling
- Add images to `src/img/` directory
