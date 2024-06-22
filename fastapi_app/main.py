from fastapi import FastAPI
from pydantic import BaseModel
import os
from data_downloader.uploading_files import download_file, unzip_file, decompress_gz_files, decompress_z_files, convert_crx_to_rnx

app = FastAPI()

class SatelliteRequest(BaseModel):
    satellite_name: str

@app.post("/request_satellite_data/")
def request_satellite_data(request: SatelliteRequest):
    date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    file_name = f"{date}.zip"
    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    
    download_file(link, file_name)
    unzip_file(file_name, date)
    decompress_gz_files(date)
    decompress_z_files(date)
    convert_crx_to_rnx(date)
    
    return {"message": f"Данные для спутника {request.satellite_name} успешно загружены и обработаны."}

