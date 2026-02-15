from fastapi import APIRouter

from logger import get_logger


logger = get_logger(__name__)

app_endpoints = APIRouter()