import requests

def check_security(url):
    results = {}
    
    # Check for Cross-Site Scripting (XSS)
    xss_payload = "<script>alert('XSS vulnerability')</script>"
    xss_response = requests.get(url + xss_payload)
    if xss_payload in xss_response.text:
        results["XSS Vulnerability"] = "Detected"
    else:
        results["XSS Vulnerability"] = "Not Detected"
    
    # Check for SQL Injection
    sql_payload = "1' OR '1'='1"
    sql_response = requests.get(url + "?id=" + sql_payload)
    if "Error" in sql_response.text:
        results["SQL Injection Vulnerability"] = "Detected"
    else:
        results["SQL Injection Vulnerability"] = "Not Detected"
    
    # Check for Insecure Direct Object References
    insecure_payload = "admin"
    insecure_response = requests.get(url + "/" + insecure_payload)
    if "Unauthorized" in insecure_response.text:
        results["Insecure Direct Object Reference"] = "Detected"
    else:
        results["Insecure Direct Object Reference"] = "Not Detected"
    
    return results
