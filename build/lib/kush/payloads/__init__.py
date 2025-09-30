# kush-framework/kush/payloads/__init__.py
"""
Payload generators
"""

from kush.payloads.windows import WindowsPayload
from kush.payloads.linux import LinuxPayload
from kush.payloads.macos import MacOSPayload
from kush.payloads.templates import VBSTemplate, PythonTemplate

__all__ = ['WindowsPayload', 'LinuxPayload', 'MacOSPayload', 'VBSTemplate', 'PythonTemplate']
