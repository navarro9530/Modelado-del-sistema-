#la entrada principal de nuestro proyecto 

#para ejecutar la aplicacion desde la consola debemos cocuemtar la sigiente linea 
#venv\Scripts\uvicorn main:app --reload

#la documentacion interativa queda la siguente 
#http://localhost:8000/docs <-- swagger
#http://localhost:8000/redoc <-- redoc

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scr.api.router import router

app = FastAPI(
    title="IUTEDE - Gestion de TICS",
    description="Api para la gestion de los recursos TIC de la Utede",
    version="1.0"
    )

#Middleware Cors permite que el fromt 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "api": "iutede backend", "version": "1.0.0"}