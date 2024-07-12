import pdb

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to execute before the view is called
        print(f"Middleware: Before view processing - {request.path}")
        #pdb.set_trace()  # Set breakpoint here
        
        response12 = self.get_response(request)
        
        # Code to execute after the view is called
        print(f"Middleware: After view processing - {request.path}")
        #pdb.set_trace()  # Set breakpoint here
        
        return response12