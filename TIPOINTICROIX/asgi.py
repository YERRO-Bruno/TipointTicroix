"""
ASGI config for TIPOINTICROIX project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import asyncio
from server3 import main

if __name__ == "__main__":
    asyncio.run(main())