from rest_framework.views import exception_handler
import re

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 400:
        required_fields = []
        error_message = None

        for field, messages in response.data.items():
            if field == "non_field_errors":
                error_msg = messages[0]
                if "Must include" in error_msg:
                    # Extract fields between quotes for missing fields error
                    required_fields.extend(re.findall(r'"([^"]*)"', error_msg))
                elif "Unable to log in with provided credentials" in error_msg:
                    # Handle invalid login credentials error
                    error_message = "Invalid email or password"
            else:
                # Handle signup/regular field errors
                if isinstance(messages, list) and any(
                    "This field is required." in msg for msg in messages
                ):
                    required_fields.append(field)
                else:
                    # Handle other field errors like duplicate username
                    if isinstance(messages, list):
                        error_message = messages[0]

        # Set the response data based on the type of error
        if required_fields:
            response.data = {"message": f"Please provide: {', '.join(required_fields)}"}
        elif error_message:
            response.data = {"message": error_message}

    return response
