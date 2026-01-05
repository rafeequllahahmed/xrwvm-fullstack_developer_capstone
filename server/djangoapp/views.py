# start

from .restapis import get_request, analyze_review_sentiments, post_review
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import CarMake, CarModel
from .populate import initiate
from django.http import JsonResponse
import json
from django.contrib.auth import login, authenticate
import logging
from django.views.decorators.csrf import csrf_exempt


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
@csrf_exempt
@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"}
            )
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
