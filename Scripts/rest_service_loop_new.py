import requests, argparse, json, time

# Setup arguments
parser = argparse.ArgumentParser(description='Loop Rest call until desire response is reached') 
parser.add_argument('-url','-u', action="store", dest="url", help='REST Service URL')
parser.add_argument('-headerdata','-p', action="store", dest="headerdata", help='Headers')
parser.add_argument('-method','-m', action="store", dest="rest_method", help='REST Method')
parser.add_argument('-body','-b', action="store", dest="body", help='REST Body if method requires it')
parser.add_argument('-variable','-x', action="store", dest="variable", help='Variable Name storing response')
parser.add_argument('-value','-y', action="store", dest="value", help='Desired value to break loop')
#parser.add_argument('-output','-o', action="store", dest="output", help='Name of JSON output file e.g. output.json')
args = parser.parse_args()

def rest_loop(url, method,  body, headers, variable, value):
    print("starting rest loop")

    result = ''
    _break = False

    while result != value:
        response = call_rest_service(url, method,body,headers)
        result = parse_response(response.json(), variable)
        print("Result: " + str(result) + " Desired: " + str(value))
        time.sleep(5)

        if _break:
            break


def call_rest_service(url, method,  body, headers):
    print("starting rest call")
    _headers = ""
    if bool(body):
        print("body found")
        data = json.loads(body)

    if bool(headers):
        print("headers found")
        _headers = json.loads(headers)

    if method == "GET":
        print("GET method")
        response = requests.get(url, headers =_headers)
        print(response.json())
        print(response.request.headers)
        return response
    elif method == "POST":
        print("POST method")
        response = requests.post(url, data = data, headers = _headers)
        print(response.json())
        print(response.request.headers)
        return response

    print("starting rest call")

def parse_response(data, variable):
    print("parsing result")
    print(data)
    job = data['job']
    print(job)

    print(job[variable])
    return job[variable]
    




##
##	Main execution 
##
def main():
    print("Main execution started")
    rest_loop(args.url, args.rest_method,  args.body, args.headerdata, args.variable, args.value)


if __name__ == "__main__":
    main()