"""
Network connectivity checker for automatic online/offline mode switching.
"""
import socket
import threading
from typing import Callable, Optional

class NetworkChecker:
    """Check internet connectivity and notify on status changes."""
    
    def __init__(self):
        self._is_online = False
        self._check_lock = threading.Lock()
        self._callbacks: list[Callable[[bool], None]] = []
    
    def check_internet(self, timeout: float = 3.0) -> bool:
        """
        Check if internet is available.
        Uses Google's DNS server as a reliable endpoint.
        """
        with self._check_lock:
            try:
                # Try to connect to Google's DNS
                socket.setdefaulttimeout(timeout)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
                self._is_online = True
            except (socket.error, socket.timeout, OSError):
                # Try backup: Cloudflare DNS
                try:
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("1.1.1.1", 53))
                    self._is_online = True
                except (socket.error, socket.timeout, OSError):
                    self._is_online = False
            
            return self._is_online
    
    @property
    def is_online(self) -> bool:
        """Get cached online status."""
        return self._is_online
    
    def add_status_callback(self, callback: Callable[[bool], None]):
        """Add a callback to be notified of status changes."""
        self._callbacks.append(callback)
    
    def notify_status_change(self):
        """Notify all callbacks of current status."""
        for callback in self._callbacks:
            try:
                callback(self._is_online)
            except Exception:
                pass

# Global instance
_network_checker: Optional[NetworkChecker] = None

def get_network_checker() -> NetworkChecker:
    """Get the global network checker instance."""
    global _network_checker
    if _network_checker is None:
        _network_checker = NetworkChecker()
    return _network_checker

def is_online() -> bool:
    """Quick check if internet is available."""
    return get_network_checker().check_internet()
