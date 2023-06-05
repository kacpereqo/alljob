import uvicorn
from config import import_routers
from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def get_app() -> FastAPI:
    app = FastAPI()
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    import_routers(app)

    return app


app = get_app()


if __name__ == "__main__":
    env = dotenv_values()

    host = env.get("HOST", "8080")
    port = int(env.get("PORT", "8080"))

    uvicorn.run("main:app", host=host, port=port, reload=True)
