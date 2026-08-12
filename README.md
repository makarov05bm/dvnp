# dvnp

## What is Damn Vulnerable NGINX Proxy?
A self-contained web security lab that simulates a multi-host NGINX reverse-proxy environment. It connects an attacker to multiple virtual hosts, backend Flask applications, and shared resources, providing a realistic environment for exploring chained web and reverse-proxy misconfigurations.
<br/>
<br/>
<img width="1672" height="941" alt="3970a670-ad30-4a55-89b0-f653b00d70fd" src="https://github.com/user-attachments/assets/ac3313e0-3f3b-4b53-b6a0-af4b0a3596d2" />

## Lab Architecture
<img width="1598" height="984" alt="c28b2cec-cc6c-4220-9168-167264b62b50" src="https://github.com/user-attachments/assets/977b0e5b-9a9b-4624-961f-c6b4d5d06461" />

## Lab Set Up
```shell
git clone https://github.com/makarov05bm/dvnp.git
cd dvnp
```

**Add the vhosts entries to `/etc/hosts` to use domain names instead of IP addresses:**
```shell
sudo nano /etc/host

127.0.0.1 portal.skyblue.com
127.0.0.1 sandbox-dev-001.skyblue.com
127.0.0.1 sandbox-dev-002.skyblue.com
```

**Run the lab:**
```shell
docker compose up --build --force-recreate --remove-orphans
```

**Verify all three vhosts are up:**
```shell
curl -I "http://portal.skyblue.com:8090/"
curl -I "http://sandbox-dev-001.skyblue.com:8090/"
curl -I "http://sandbox-dev-002.skyblue.com:8090/"
```

## Lab Solutions Guide
You can find all documented findings explained from a black and white-box perspective at my [blog](https://blog.oussmess.me/posts/damn-vulnerable-nginx-proxy-full-guide)

## Suggestion
I welcome any suggestions or additions, fixes, etc. Feel free to open a PR, reach out to me for feedback, suggestions, questions...
I hope you enjoy working through the lab, then I want to see you go hunt those boring NGINX servers that you were leaving for later :)
