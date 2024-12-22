import os
import xml.etree.ElementTree as ET

from flask import Blueprint, request, jsonify
from model.solicitante import Solicitante

Usuario = Blueprint('usuarios', __name__)