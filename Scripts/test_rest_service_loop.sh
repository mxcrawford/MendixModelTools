#python rest_service_loop.py \
#-url "https://deploy.mendix.com/api/1/apps/cicd-demo/packages/8a3d982c-900c-4f26-874d-3c6f4232443e" \
#-method "GET" \
#-headerdata "{\"Mendix-Username\": \"alistair.crawford@mendix.com\",\"Mendix-ApiKey\":\"bb46dd3c-1696-4a1d-8bfc-6b30d432a0bf\", \"Content-Type\":\"application\/json\"}" \
#-variable "Status" \
#-value "Succeeded"

python rest_service_loop.py \
-url "https://deploy.mendix.com/api/1/apps/cicd-demo/environments/Acceptance/start/f0566a30-1e6b-436f-80f8-c4b56e1ef5af" \
-method "GET" \
-headerdata "{\"Mendix-Username\": \"alistair.crawford@mendix.com\",\"Mendix-ApiKey\":\"bb46dd3c-1696-4a1d-8bfc-6b30d432a0bf\", \"Content-Type\":\"application\/json\"}" \
-variable "Status" \
-value "Succeeded"