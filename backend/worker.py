#!/usr/bin/env python
"""
Celery worker for executing training jobs

Usage:
    python worker.py

Or with specific options:
    celery -A tasks worker --loglevel=info --concurrency=1
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from tasks import celery_app

if __name__ == '__main__':
    # Start worker
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--concurrency=1',  # One job at a time (GPU limitation)
        '--pool=solo'  # Use solo pool for compatibility
    ])
