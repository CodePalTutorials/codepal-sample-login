from __future__ import print_function


class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        import traceback
        print(traceback.format_exc())
