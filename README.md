# DVNP

## What is Damn Vulnerable NGINX Proxy?
A self-contained web security lab that simulates a multi-host NGINX reverse-proxy environment. It connects an attacker to multiple virtual hosts, backend Flask applications, and shared resources, providing a realistic environment for exploring chained web and reverse-proxy misconfigurations.
<br/>
<br/>
<img width="1672" height="941" alt="187e8f86-2b3c-46f3-8795-263b9af31c52" src="https://github.com/user-attachments/assets/351194cb-6cf0-44cf-b33c-dbe87e41eb06" />

## Lab Architecture
<img width="1598" height="984" alt="c28b2cec-cc6c-4220-9168-167264b62b50" src="https://github.com/user-attachments/assets/977b0e5b-9a9b-4624-961f-c6b4d5d06461" />

## Misconfigurations / Exploit Chains Covered

The lab chains together 20 independent findings, spanning:

1. Authorization Bypass via a Permissive Alternate Root
2. Broken Access Control via Trim Inconsistencies
3. HTTP Splitting via Unsanitized Regex Capture Leads to Open Redirect
4. Path Traversal / LFI via Root proxy_pass Without Upstream URI
5. Authorization Bypass via Unvalidated Regex Capture in proxy_pass
6. IP Spoofing via Missing proxy_set_header Inheritance
7. Denial of Service via Unbounded Request Body
8. CORS Misconfiguration via Missing Regex Anchor
9. Open Redirect via User-Registerable Cloud Storage Bucket Name
10. Access Control Bypass due to Default-Allow Gap in the map Directive and merge_slashes=off
11. Cache Poisoning via Client-Controlled X-Forwarded-Host Header and Unkeyed Input
12. Web Cache Deception via Extension-Based Cache Matching
13. Location Match-Priority Bypass via ^~ Overriding a Regex deny Rule
14. Blind Stored XSS via Unescaped Log Injection
15. Information Disclosure via Exposed stub_status
16. Open Redirect via Missing Leading Slash in a Rewrite Capture Group
17. Access Control Inconsistency due to auth_basic Not Inherited by a More-Specific Location
18. Authentication Bypass via satisfy any and a Broken IP Trust Boundary
19. Credential Brute-Force via Missing Rate Limiting on Basic Auth
20. Credential Reuse Across Trust Boundaries via a Shared .htpasswd File

Some findings only become exploitable *because* of another misconfiguration elsewhere in the same config; part of the point of this lab is learning to spot those interaction effects, not just isolated bugs.

## Lab Set Up
```shell
git clone https://github.com/makarov05bm/dvnp.git
```

**Add the vhosts entries to `/etc/hosts` to use domain names instead of IP addresses:**
```shell
sudo nano /etc/host

127.0.0.1 portal.skyblue.com
127.0.0.1 sandbox-dev-001.skyblue.com
127.0.0.1 sandbox-dev-002.skyblue.com
```

**Run the lab:**
- Running the HTTP version
```shell
cd dvnp-http
docker compose up --build --force-recreate --remove-orphans
```

- Running the HTTPS version
```shell
cd dvnp-ssl
docker compose up --build --force-recreate --remove-orphans
```

**Verify all three vhosts are up:**
```shell
curl -I "http://portal.skyblue.com:8090/"
curl -I "http://sandbox-dev-001.skyblue.com:8090/"
curl -I "http://sandbox-dev-002.skyblue.com:8090/"
```
OR if running the HTTPS version
```
curl -I "https://portal.skyblue.com:8090/"
curl -I "https://sandbox-dev-001.skyblue.com:8090/"
curl -I "https://sandbox-dev-002.skyblue.com:8090/"
```

## Lab Solutions Guide
You can find all documented findings explained from a black and white-box perspective at my [blog](https://blog.oussmess.me/posts/damn-vulnerable-nginx-proxy-full-guide)

## Suggestions
I welcome any suggestions or additions, fixes, etc. Feel free to open a PR, reach out to me for feedback, suggestions, questions...
I hope you enjoy working through the lab, then I want to see you go hunt those boring NGINX servers that you were leaving for later :)

## References
https://nginx.org/en/docs/dirindex.html

https://snyk.io/blog/url-confusion-vulnerabilities/#slash

https://blog.detectify.com/industry-insights/common-nginx-misconfigurations-that-leave-your-web-server-ope-to-attack/

https://labs.detectify.com/ethical-hacking/middleware-middleware-everywhere-and-lots-of-misconfigurations-to-fix/

https://hacktricks.wiki/en/network-services-pentesting/pentesting-web/nginx.html#http2-upstream-request-injection-with-proxy_set_body

https://blog.bugport.net/exploiting-http-parsers-inconsistencies

https://tolo7010note.blogspot.com/2020/07/an-unreproducable-bug-due-to-load.html
