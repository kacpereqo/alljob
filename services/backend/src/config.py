from offerts.routes import router as offerts_router


def import_routers(app):
    app.include_router(offerts_router)
