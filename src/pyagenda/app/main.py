import uvicorn
from fastapi import FastAPI

from pyagenda.app.api_router import api_router
from pyagenda.app.core.config import config


def new_app() -> FastAPI:
    app = FastAPI(
        title=config.APP_NAME,
        description=config.APP_DESCRIPTION,
        version=config.APP_VERSION,
        docs_url="/docs",
        debug=config.DEBUG,
    )

    app.include_router(api_router)

    return app


app = new_app()

if __name__ == "__main__":
    uvicorn.run(
        "pyagenda.app.main:new_app", host="0.0.0.0", port=config.PORT, reload=True
    )
