#!/bin/bash
set -e

# =========================================================
# Step 1: Wait for apt locks to be released
echo "Waiting for apt locks to be released..."
while sudo fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1; do
    echo "Apt lock is held by another process, waiting..."
    sleep 1
done

# =========================================================
# Step 2: Update package list and install system dependencies
echo "Updating package list..."
sudo apt update

echo "Installing required system packages (python3, python3-pip, git, chromium-browser, xvfb)..."
sudo apt install -y python3 python3-pip git chromium-browser xvfb

# =========================================================
# Step 3: Upgrade pip and install required Python packages
echo "Upgrading pip (using --break-system-packages)..."
python3 -m pip install --upgrade pip --break-system-packages

echo "Installing required Python packages (selenium, pandas, webdriver-manager) using --break-system-packages..."
python3 -m pip install selenium pandas webdriver-manager --break-system-packages

# =========================================================
# Step 4: Clone or update your GitHub repository
# Replace the following URL with your repository's URL.
REPO_URL="https://github.com/nallavallidhanunjaya/dharma-job-notifier.git"
# The expected repository directory (update if needed)
REPO_DIR="dharma-job-notifier"

if [ -d "$REPO_DIR" ]; then
    echo "Repository already exists. Pulling the latest changes..."
    cd "$REPO_DIR"
    git pull
    cd ..
else
    echo "Cloning repository from GitHub..."
    git clone "$REPO_URL"
fi

# =========================================================
# Step 5: Export email credentials for send_email.py
# Setting these as environment variables helps secure sensitive information.
# Make sure these values match your intended sender, app password, and recipient.
export EMAIL_FROM="nallavallidharmateja92@gmail.com"
export EMAIL_PASSWORD="feknevawqvfzuani"
export EMAIL_TO="dharmanallavalli@gmail.com"

# =========================================================
# Step 6: Execute the Python scripts in sequence
cd "$REPO_DIR"

# Run scraper.py with xvfb-run so that headless Chromium works on a server
echo "Running scraper.py..."
xvfb-run -a python3 scraper.py

# Run filterjobposting.py to process the scraped CSV data
echo "Running filterjobposting.py..."
python3 filterjobposting.py

# Run send_email.py to email the filtered CSV file
echo "Running send_email.py..."
python3 send_email.py

echo "All scripts executed successfully."
