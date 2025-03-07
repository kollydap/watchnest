from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {
            "status": renderer_context["response"].status_code,
            "message": (
                "Successful"
                if renderer_context["response"].status_code < 400
                else "Error"
            ),
            "data": data,
        }
        return super().render(response, accepted_media_type, renderer_context)
