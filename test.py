import httplib2
import socks


socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1")
socks.wrapmodule(httplib2)
h = httplib2.Http()
r,c = h.request("http://www.google.com")