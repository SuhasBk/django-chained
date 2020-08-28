import os
from threading import Thread
from subprocess import run, PIPE
from rest_framework.views import APIView
from rest_framework.response import Response

GLOBAL_ERROR_MESSAGE = ''

class DeccanApi(APIView):

    def get(self, request):
        edition = request.query_params.get('edition')

        def spinoff():
            global GLOBAL_ERROR_MESSAGE
            op = run(['python3', 'dh_selenium.py', edition],stdout=PIPE, stderr=PIPE)
            errors = op.stderr.decode('utf-8')

            if errors:
                GLOBAL_ERROR_MESSAGE = errors
            
            return

        if not edition:
            return Response({
                'response': {
                    '/api/deccan?edition=': {
                        0: 'Bangalore',
                        1: 'Davanagere',
                        2: 'Gadag, Haveri, Ballari',
                        3: 'Hubballi-Dharwad',
                        4: 'Kalaburgi',
                        5: 'Kolar, Chikkaballapur, Tumkuru',
                        6: 'Mangaluru',
                        7: 'Mysuru',
                        8: 'Uttara Kannada, Belagavi City'
                    }
                }
            }, 200)
        else:
            Thread(target=spinoff).start()
            return Response({
                'response': f'epaper{edition}.pdf'
            }, 200)


class FileExists(APIView):
    def get(self, request):
        global GLOBAL_ERROR_MESSAGE
        file_name = request.query_params.get('file')
        list_of_files = os.listdir()
        
        if file_name in list_of_files:
            return Response({'response': True}, 200)
        elif GLOBAL_ERROR_MESSAGE:
            errors = GLOBAL_ERROR_MESSAGE
            GLOBAL_ERROR_MESSAGE = ''
            return Response({'response': False, 'errors': errors})
        else:
            return Response({'response': False, 'ls': list_of_files }, 200)

class Testing(APIView):
    def get(self, request, format=None):
        return Response({ 'response': 'hi' }, 200)
