import gunicorn
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# 컨트롤 라우터 선언
from total_analysis import total_analysis_router
from diff_analysis import diff_analysis_router
from dash_area_info import dash_area_info_router
from auth import auth_router

app = FastAPI(
    title="Gasi Dash Board",
    version="0.0.1",
)
# cors allow path
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://ec2-3-34-7-93.ap-northeast-2.compute.amazonaws.com:3000/",
    "http://ec2-3-34-7-93.ap-northeast-2.compute.amazonaws.com:3000",
]
# cors settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(dash_area_info_router.router)
app.include_router(total_analysis_router.router)
app.include_router(diff_analysis_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8892, reload=True)
