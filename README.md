# wolpage
simple page to send wake-on-lan magic packets with.

## notes
this project is written with `quart`, not `flask`. therefore, you need to use
an ASGI runtime, not WSGI.

the service unit and setup guide has been written with `hypercorn` as the 
ASGI runtime in mind. if you prefer another runtime such as `uvicorn` or 
`granian`, ignore all mentions of hypercorn and setup your preferred runtime 
instead.

## dependencies
make sure your system has `python3-pyotp`, `python3-quart`, `etherwake`, `python3-hypercorn` and `python3` installed.

debian/ubuntu/rpios:
```sh
apt install -y python3-pyotp python3-quart python3-hypercorn etherwake
```

## installation
- create a user: `useradd -M wolpage`
- add `wolpage ALL=NOPASSWD: /usr/sbin/etherwake` to `/etc/sudoers`
- copy the `wolpage` folder to `/opt/`
- let `wolpage` own the folder: `chown -R wolpage:wolpage /opt/wolpage`
- navigate to `/opt/wolpage`
- create your config from the template: `mv conf.template.toml conf.toml`
- edit `conf.toml` to add the settings
  - `title`     -- the title that shows up in the titlebar and on the page heading.
  - `secret`    -- your topt secret - use something long and secure!! note it down for later.
  - `pc_mac`    -- the target mac address - must use colons as seperators!
  - `interface` -- the network interface to send the packet from; check ifconfig
- copy `wolpage.service` to `/etc/systemd/system` with `cp wolpage.service /etc/systemd/system/wolpage.service`
- reload systemd so it loads `wolpage.service`: `systemctl daemon-reload`
- enable and start the service: `systemctl enable --now wolpage.service`
- setup your reverse proxy to point to `127.0.0.1:30303`

## provisioning
- open the python repl: `python3`
```py
>>> import pyotp
>>> pyotp.totp.TOTP('my_secret').provisioning_uri(issuer_name='wol')
'otpauth://totp/wol:Secret?secret=my_secret&issuer=wol'
```
- encode the link in a trustworthy QR Code encoder (e.g. zbar, [this](https://kazuhikoarase.github.io/qrcode-generator/js/demo/))
- scan the resulting QR Code into your OTP manager (e.g. FreeOTP, andOTP, Google Authenticator)
