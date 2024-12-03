from exceptions import AuthException, BadRequestException, NotFoundException, InternalServerException, UserAlreadyExistsException, TrialExpiredException

class ExceptionHandler:

    @staticmethod
    def handle_exception(e: Exception, message: str) :
        if type(e) in [AuthException, BadRequestException, NotFoundException, InternalServerException, UserAlreadyExistsException, TrialExpiredException]:
            return {    
                "message": message,
                "error": e.error
            }, e.status_code
        return {
            "message": "An Unexpected Error Occured",
            "error": str(e)
        }, 500