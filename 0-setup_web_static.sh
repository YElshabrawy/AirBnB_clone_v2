#!/usr/bin/env bash
# ##

# Install Nginx if it not already installed
if ! which nginx &> /dev/null
then
	sudo apt-get -y update
	sudo apt-get -y install nginx
fi

# Function to create directories if they don't exist
create_dir() {
    if [ ! -d "$1" ]; then
        sudo mkdir -p "$1"
    fi
}

# Create necessary directories
directories=(
    "/data/"
    "/data/web_static/"
    "/data/web_static/releases/"
    "/data/web_static/shared/"
    "/data/web_static/releases/test/"
)

for dir in "${directories[@]}"; do
    create_dir "$dir"
done

# Create a fake HTML file
echo "Hello World! Youssef was here!" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
content="location /hbnb_static/ {\n\talias /data/web_static/current/;\n\t}"
sudo sed -i "s|server_name _;|server_name _;\n\t$content|" /etc/nginx/sites-available/default

# Restart Nginx
sudo /etc/init.d/nginx restart
