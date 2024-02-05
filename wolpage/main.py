import pyotp
import tomllib as toml
import subprocess
from quart import Quart, render_template, request

def create_app():
    app = Quart(__name__)

    @app.get("/")
    async def page():
        return await render_template("./index.j2")

    @app.post("/")
    async def post():
        try:
            conf = {}
            r = await request.form
            p = r.get('otp')

            with open("./conf.toml", "rb") as f:
                conf = toml.load(f);

            totp = pyotp.TOTP(conf["secret"])

            if totp.verify(p):
                ret = subprocess.call(f"sudo etherwake {conf['pc_mac']} -i {conf['interface']}", shell=True)

                if ret != 0:
                    return await render_template("./index.j2", err=True, title=conf["title"])
                
                return await render_template("./index.j2", ok=True, title=conf["title"])
            else:
                return await render_template("./index.j2", wrong=True, title=conf["title"])
        except Exception as e:
            print(e)
            return await render_template("./index.j2", err=True, title=conf["title"])

    return app

if __name__ == "__main__":
    create_app().run()
