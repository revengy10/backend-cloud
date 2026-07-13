import io

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from PIL import Image


def _get_uploaded_image(request):
    """Extract the uploaded image from a multipart POST request."""
    if "image" not in request.FILES:
        return None
    try:
        return Image.open(request.FILES["image"])
    except Exception:
        return None


@csrf_exempt
def get_resolution(request):
    """Return the resolution of the uploaded image as JSON."""
    if request.method != "POST":
        return HttpResponseBadRequest("Send a POST request with an 'image' file.")
    img = _get_uploaded_image(request)
    if img is None:
        return HttpResponseBadRequest("No valid 'image' file found in request.")
    width, height = img.size
    return JsonResponse({"width": width, "height": height})


@csrf_exempt
def convert_grayscale(request):
    """Convert the uploaded image to grayscale and return it as PNG."""
    if request.method != "POST":
        return HttpResponseBadRequest("Send a POST request with an 'image' file.")
    img = _get_uploaded_image(request)
    if img is None:
        return HttpResponseBadRequest("No valid 'image' file found in request.")
    gray = img.convert("L")
    buf = io.BytesIO()
    gray.save(buf, format="PNG")
    return HttpResponse(buf.getvalue(), content_type="image/png")