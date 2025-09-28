#!/usr/bin/env python3
"""
aiohttp Static File Server - Path Traversal Security Demo

This script demonstrates how improper configuration of static file serving
can lead to path traversal vulnerabilities.

SECURITY WARNING: This is for educational purposes only. Never use 
follow_symlinks=True in production without proper security measures.
"""

import os
import sys
import asyncio
from pathlib import Path
from aiohttp import web

# Server configuration
HOST = '127.0.0.1'
PORT = 8080
STATIC_DIR = 'static'
PRIVATE_DIR = 'private'

async def create_demo_files():
    """Create demonstration files and directories"""
    
    # Create static directory with legitimate files
    static_path = Path(STATIC_DIR)
    static_path.mkdir(exist_ok=True)
    
    # Create some legitimate static files
    (static_path / 'index.html').write_text('''
<!DOCTYPE html>
<html>
<head>
    <title>Static Server Demo</title>
</head>
<body>
    <h1>Welcome to the Static Server</h1>
    <p>This is a legitimate static file.</p>
    <ul>
        <li><a href="/static/style.css">style.css</a></li>
        <li><a href="/static/script.js">script.js</a></li>
    </ul>
</body>
</html>
    '''.strip())
    
    (static_path / 'style.css').write_text('''
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
    '''.strip())
    
    (static_path / 'script.js').write_text('''
console.log('This is a legitimate JavaScript file');
    '''.strip())
    
    # Create private directory with sensitive files (outside static)
    private_path = Path(PRIVATE_DIR)
    private_path.mkdir(exist_ok=True)
    
    (private_path / 'secrets.txt').write_text('''
SENSITIVE INFORMATION
=====================
API_KEY=super_secret_key_12345
DATABASE_PASSWORD=admin123
PRIVATE_TOKEN=xyz789abc

This file should NOT be accessible via the web server!
    '''.strip())
    
    (private_path / 'config.json').write_text('''
{
    "database": {
        "host": "internal.db.server",
        "port": 5432,
        "username": "admin",
        "password": "secret_password"
    },
    "internal_api": {
        "endpoint": "http://internal-api:8000",
        "token": "bearer_token_xyz"
    }
}
    '''.strip())
    
    print(f"✓ Created static directory: {static_path.absolute()}")
    print(f"✓ Created private directory: {private_path.absolute()}")
    print(f"✓ Created demo files in both directories")

async def init_app():
    """Initialize the aiohttp application"""
    app = web.Application()
    
    # SECURITY WARNING: follow_symlinks=True can lead to path traversal!
    # This is intentionally vulnerable for demonstration purposes
    app.router.add_static(
        '/static/', 
        path=STATIC_DIR,
        follow_symlinks=True,  # VULNERABLE SETTING!
        append_version=False
    )
    
    # Add a root handler
    async def index(request):
        return web.Response(text='''
<!DOCTYPE html>
<html>
<head>
    <title>aiohttp Static Server Demo</title>
</head>
<body>
    <h1>aiohttp Static Server</h1>
    <p>Static files are served from <code>/static/</code></p>
    <p><a href="/static/index.html">View static index.html</a></p>
    
    <h2>Security Note</h2>
    <p>This server has <code>follow_symlinks=True</code> which can lead to path traversal vulnerabilities!</p>
    
    <h2>Testing Path Traversal</h2>
    <pre>
# Legitimate request:
curl http://127.0.0.1:8080/static/index.html

# Path traversal attempt (may work with follow_symlinks=True):
curl --path-as-is http://127.0.0.1:8080/static/../private/secrets.txt
    </pre>
</body>
</html>
        ''', content_type='text/html')
    
    app.router.add_get('/', index)
    
    return app

def print_security_warning():
    """Print security warnings and usage instructions"""
    print("\n" + "="*60)
    print("SECURITY WARNING - EDUCATIONAL PURPOSES ONLY")
    print("="*60)
    print("This server is intentionally vulnerable to path traversal!")
    print("Never use follow_symlinks=True in production without proper")
    print("security measures like path validation and sandboxing.")
    print("="*60 + "\n")

def print_usage_instructions():
    """Print usage instructions for testing"""
    print(f"\n✓ Server running at http://{HOST}:{PORT}")
    print("\nTest commands:")
    print("-" * 40)
    print("1. Normal static file access:")
    print(f"   curl http://{HOST}:{PORT}/static/index.html")
    print(f"   curl http://{HOST}:{PORT}/static/style.css")
    print()
    print("2. Path traversal attempts:")
    print(f"   curl --path-as-is http://{HOST}:{PORT}/static/../private/secrets.txt")
    print(f"   curl --path-as-is http://{HOST}:{PORT}/static/../../etc/passwd")
    print()
    print("3. URL encoded traversal:")
    print(f"   curl http://{HOST}:{PORT}/static/%2e%2e/private/secrets.txt")
    print()
    print("4. Double encoding attempt:")
    print(f"   curl http://{HOST}:{PORT}/static/%252e%252e/private/secrets.txt")
    print("-" * 40)
    print("\nPress Ctrl+C to stop the server\n")

async def main():
    """Main function to run the server"""
    # Create demo files
    await create_demo_files()
    
    # Print warnings
    print_security_warning()
    
    # Initialize and start the app
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()
    
    # Print usage instructions
    print_usage_instructions()
    
    # Keep the server running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
    finally:
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
