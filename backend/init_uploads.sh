#!/bin/bash
# Initialize uploads directory with correct permissions

echo "Initializing uploads directory..."

# Create uploads directory if it doesn't exist
mkdir -p /app/uploads_temp

# Change ownership to appuser
chown -R appuser:appuser /app/uploads_temp

# Set proper permissions
chmod -R 755 /app/uploads_temp

echo "Uploads directory initialized with permissions:"
ls -la /app/uploads_temp/

# Start the application
exec "$@"