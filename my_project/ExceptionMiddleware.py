from django.utils.deprecation import MiddlewareMixin


class ConsoleExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        import traceback
        import sys
        exc_info = sys.exc_info()
        print "######################## Exception #############################"
        print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
        print "################################################################"
        print repr(request)
        #print "################################################################"

