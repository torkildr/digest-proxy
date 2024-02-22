## HTTP Digest Proxy

This is a simple proxy with a very simple use case.

I was in need of a way to strip away HTTP Digest Authentication, so that I
could reverse proxy an internal service and put it behind SSO.

As far as I can tell, Caddy does not support this. Neither does nginx.

When you run this proxy, it will pass the requests along to the upstream server
with bolted on digest credentials. It will in other words strip it away.

The docker images wraps both the fastcgi and reverse proxy in one, so that it
presents a coherent endpoint you can either call directly or further reverse
proxy.

### An example docker compose config:

```
service:
  digest-proxy:
    build:
        context: digest-proxy
    restart: unless-stopped
    expose:
      - '80'
    environment:
      - DIGEST_USER=username
      - DIGEST_PASSWORD=password
      - PROXY_HOST=http://digest-protected-host.lan
```

### How does it work?

When running the container as in the example above, you can make a request to the proxy:
```
curl http://localhost:80/foobar
```

The digest-proxy will then make a new request, literally using curl, to the upstream service
```
curl --digest --user username:password http://digest-protected-host.lan/foobar
```

### How safe is it?

Not very. Please be careful. This is bolted together with duct tape, string and chewing gum.
Please don't expect it to be production quality.

It has been tested with `GET`, `DELETE`, `PUT` `POST` etc, with and without
binary payloads in all directions. Headers should mostly propagate correctly in all directions.

There is little reason to think that there _aren't_ any
edge cases, though.

