import nox

nox.options.sessions = ["lint"]
locations = "rarity_tools_scraper_api", "rarity_tools_scraper_lib", "noxfile.py"


@nox.session(python="3.9")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
