package httpapi.authz

# HTTP API request
import input
# input = {
#   "method": "GET",
#   "device": "Android"
# }

default allow = false

# Allow users to access site only 
# if they use the following device.
allow {
  input.method = "GET"
  input.device == "Apple"
}