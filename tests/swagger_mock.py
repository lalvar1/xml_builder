swagger = """
 {"info": {"title": "cases","version": "v1"},"openapi": "3.0.1","paths":
  {"SanCaseCreation": {"get": {"responses": {"default": {"content":
  {"application/json": {"schema": {"type": "string"}}},"description":
  "Response"}}},"post": {"tags": ["FCP-Work-OutReach"]}},"requestBody":
  {"CustomerLegalName": "string","EmailID": "string","Event":
  "string","JNumber": "string","KYCPegaCaseID": "string","ORCaseID":
  "string","content": {"application/json": {"schema": {"type":
  "string"}}},"description": "Request"},"responses": {"default": {"content":
  {"application/json": {"schema": {"type": "string"}}},"description":
  "Response"},"tags": ["FCP-SAN-OR-Work-OutReach"]}},"security":
  [{"authentication": []}],"servers": [{"url":
  "https://cloud.net/prweb/PRRestService/SanOutreachPortal/01.01.02/"}],"tags":
  [{"name": "Outreach"}]}
"""