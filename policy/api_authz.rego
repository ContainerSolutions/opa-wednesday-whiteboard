package httpapi.authz

# HTTP API request
import input
# input = {
#   "method": "GET",
#   "os_family": "Android"
# }

default allow = false

# Allow users to access site only 
# if they use the following os_family.
allow {
  input.method = "GET"
  input.os_family == "Apple"
}