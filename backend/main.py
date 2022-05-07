import fastapi as _fastapi
import fastapi.security as _security
from fastapi.staticfiles import StaticFiles
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas
import fastapi.openapi.docs as _docs
from fastapi.middleware.cors import CORSMiddleware
from typing import List
# import models as _models


app = _fastapi.FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
    )


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return _docs.get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return _docs.get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return _docs.get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail=f"Email {user.email} already exists"
        )

    user = await _services.create_user(user, db)
    return await _services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):

    user = await _services.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise _fastapi.HTTPException(
            status=401, detail="Invalid username or password")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return await user


@app.post('/api/leads', response_model=_schemas.Lead)
async def create_lead(
    lead: _schemas.LeadCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):

    return await _services.create_lead(user=user, db=db, lead=lead)


@app.get('/api/leads',response_model=List[_schemas.Lead])
async def  get_leads(
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.get_leads(user=user, db=db)


@app.get('/api/leads/{lead_id}',status_code=200)
async def get_lead(
    lead_id:int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.get_lead(lead_id, user, db)


@app.delete('/api/leads/{lead_id}',status_code=204)
async def delete_lead(
    lead_id:int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    await _services.delete_lead(lead_id, user, db)
    return {"Mesage":"Successfully deleted lead"}

@app.put('/api/leads/{lead_id}',status_code=200)
async def update_lead(
    lead_id:int,
    lead:_schemas.LeadCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    await _services.update_lead(lead_id, user, db, lead)
    return {"Mesage":"Successfully updated the lead"}


@app.get("/api")
async def root():
    return {"message":"Awesome Leads Manager"}