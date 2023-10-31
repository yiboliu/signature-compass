function makeGetRequest(signature) {
  let api_url = "https://signature-compass-63lof.ondigitalocean.app/get-text-signature?hex=";
  var signature_string = String(signature)
  var signature_head = signature_string.substring(0, 10)
  if (!signature_string.startsWith("0x")) {
    signature_head = signature_string.substring(0,8)
  }
  var url = api_url + signature_head
  return fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error("HTTP error! Status: ${response.status}");
      }
      return response.text();
    })
    .catch(error => {
      throw new Error("Fetch error: ${error.message}");
    });
}

module.exports = {
  makeGetRequest,
};